# pyright: basic

#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import argparse
import logging
import ipaddress
import re

from dataclasses import dataclass
from enum import Enum

import openstack.network

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib.i18n import _  # noqa

LOG = logging.getLogger(__name__)

re_port_spec = re.compile(
    r"(?:(?P<external_port>\d+):)?(?P<internal_port>\d+)(?:/(?P<protocol>\w+))?"
)


class Protocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"


@dataclass
class PortSpec:
    """Represent a port forwarding from an external port to an internal port"""

    internal_port: int
    external_port: int
    protocol: Protocol = Protocol.TCP

    def __str__(self):
        return f"{self.external_port}:{self.internal_port}/{self.protocol}"

    def __post_init__(self):
        """Apply defaults and validate attributes"""

        if self.external_port is None:
            self.external_port = self.internal_port
        if self.protocol is None:
            self.protocol = Protocol.TCP

        self.internal_port = int(self.internal_port)
        self.external_port = int(self.external_port)
        self.protocol = Protocol(self.protocol)

        for port in [self.internal_port, self.external_port]:
            if port not in range(0, 65536):
                raise ValueError(f"port {port} out of range")

    @classmethod
    def from_spec(cls, spec: str):
        """Parse a port specifiction of the form [<external_port>:]<internal_port>[/<protocol>]"""

        match = re_port_spec.match(spec)
        if not match:
            raise ValueError("invalid port forward specification")

        return cls(**match.groupdict())


def PortSpecArg(v):
    try:
        return PortSpec.from_spec(v)
    except ValueError as err:
        # argparse hides the ValueError message, and the generic message it provides
        # isn't terribly helpful. We need to convert the ValueError into something
        # that argparse will display.
        raise argparse.ArgumentTypeError(err)


class AddressOrPortArg:
    """Handle a command line argument that can be either an ip address or a port name/id"""

    def __init__(self, cli):
        self.app = cli.app

    def __call__(self, value):
        try:
            return ipaddress.ip_address(value)
        except ValueError:
            port = self.app.client_manager.sdk_connection.network.find_port(value)
            if port is None:
                raise argparse.ArgumentTypeError(f"no port with name or id {value}")
            return port

    def __repr__(self):
        return "ip address, port name, or port id"


class AddressOrNetworkArg:
    """Handle a command line argument that can be either an ip address or a network name/id"""

    def __init__(self, cli):
        self.app = cli.app

    def __call__(self, value):
        try:
            return ipaddress.ip_address(value)
        except ValueError:
            network = self.app.client_manager.sdk_connection.network.find_network(value)
            if network is None:
                raise argparse.ArgumentTypeError(f"no network with name or id {value}")
            return network

    def __repr__(self):
        return "ip address, network name, or network id"


class NetworkArg:
    """Handle a command line arguments that specifies a network name or id"""

    def __init__(self, cli):
        self.app = cli.app

    def __call__(self, value):
        network = self.app.client_manager.sdk_connection.network.find_network(value)
        if network is None:
            raise argparse.ArgumentTypeError(f"no network with name or id {value}")
        return network

    def __repr__(self):
        return "network name or id"


class SubnetArg:
    """Handle a command line argumenta that specifies a subnet name or id"""

    def __init__(self, cli):
        self.app = cli.app

    def __call__(self, value):
        subnet = self.app.client_manager.sdk_connection.network.find_subnet(value)
        if subnet is None:
            raise argparse.ArgumentTypeError(f"no subnet with name or id {value}")
        return subnet

    def __repr__(self):
        return "subnet name or id"


class NetworkOpsMixin:
    def find_floating_ip(self, address):
        connection = self.app.client_manager.sdk_connection
        if isinstance(address, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            # we were given an ip address, so find the matching floating ip
            fip = connection.network.find_ip(str(address))
            if fip is None:
                raise KeyError(f"unable to find floating ip {address}")
            return fip

        raise ValueError("invalid external ip address")

    def find_or_create_floating_ip(self, address):
        connection = self.app.client_manager.sdk_connection
        try:
            return self.find_floating_ip(address)
        except ValueError:
            # we were given a network, so attempt to create a floating ip
            fip = connection.network.create_ip(floating_network_id=address.id)

        return fip

    def find_port(self, address):
        connection = self.app.client_manager.sdk_connection
        if isinstance(address, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            # see if there exists a port with the given internal ip
            ports = list(connection.network.ports(fixed_ips=f"ip_address={address}"))

            # error out if we find multiple matches
            if len(ports) > 1:
                raise ValueError(f"found multiple ports matching address {address}")

            # if there was a single port, use it
            if len(ports) == 1:
                return ports[0]

            raise KeyError(f"unable to find port with address {address}")
        else:
            # we already have a port, so just return it
            return address

    def find_or_create_port(
        self, address, internal_ip_network=None, internal_ip_subnet=None
    ):
        connection = self.app.client_manager.sdk_connection
        try:
            return self.find_port(address)
        except KeyError:
            # we need to create a port, which means we need to know the appropriate internal network
            if internal_ip_network is None:
                if internal_ip_subnet is None:
                    raise ValueError(
                        "unable to create a port because --internal-ip-network is unset"
                    )
                internal_network_id = internal_ip_subnet.network_id
            else:
                internal_network_id = internal_ip_network.id

            # if we were given a subnet name, use it, otherwise search through subnets for an appropriate match
            if internal_ip_subnet:
                subnet = internal_ip_subnet
            else:
                for subnet in connection.network.subnets(
                    network_id=internal_network_id,
                ):
                    if subnet.ip_version != address.version:
                        continue
                    cidr = ipaddress.ip_network(subnet.cidr)
                    if address in cidr:
                        break
                else:
                    raise KeyError(f"unable to find a subnet for address {address}")

            return connection.network.create_port(
                name=f"esi-autocreated-{address}",
                network_id=internal_network_id,
                fixed_ips=[{"subnet_id": subnet.id, "ip_address": str(address)}],
            )


def port_forwarding_exists(fip, internal_ip_address, port):
    for check in fip.port_forwardings:
        fwd = openstack.network.v2.port_forwarding.PortForwarding(id="exists", **check)
        if (
            port.internal_port == fwd.internal_port
            and port.external_port == fwd.external_port
            and internal_ip_address == fwd.internal_ip_address
            and port.protocol == fwd.protocol
        ):
            return fwd


def format_forwards(func):
    """A decorator that transforms a list of (floating_ip, port_forwarding) tuples
    into a list suitable for a cliff command.Lister"""

    def wrapper(self, parsed_args):
        forwards = func(self, parsed_args)

        return [
            "ID",
            "Internal Port",
            "External Port",
            "Protocol",
            "Internal IP",
            "External IP",
        ], [
            [
                fwd[1].id,
                fwd[1].internal_port,
                fwd[1].external_port,
                fwd[1].protocol,
                fwd[1].internal_ip_address,
                fwd[0].floating_ip_address,
            ]
            for fwd in forwards
        ]

    return wrapper


class Create(command.Lister, NetworkOpsMixin):
    """Create a port forward from a floating ip to an internal address."""

    def get_parser(self, prog_name: str):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            "--description", "-d", help="Description to apply to port forwards"
        )

        parser.add_argument(
            "--internal-ip-network",
            type=NetworkArg(self),
            help=_("Network from which to allocate ports for internal ips"),
        )
        parser.add_argument(
            "--internal-ip-subnet",
            type=SubnetArg(self),
            help=_("Subnet from which to allocate ports for internal ips"),
        )
        parser.add_argument(
            "--port",
            "-p",
            type=PortSpecArg,
            action="append",
            default=[],
            help="A port mapping in the form [<external_port>:]<internal_port>[/<protocol>]. Can be specified multiple times. For example, '--port 22', '--port 80:8080', '--port 67/udp'",
        )
        parser.add_argument(
            "internal_ip_descriptor",
            type=AddressOrPortArg(self),
            help="ip address, port name, or port uuid",
        )
        parser.add_argument(
            "external_ip_descriptor",
            type=AddressOrNetworkArg(self),
            help="ip address or network name",
        )

        return parser

    @format_forwards
    def take_action(self, parsed_args: argparse.Namespace):
        if not parsed_args.port:
            raise exceptions.CommandError(
                "You must specify at least one port with --port"
            )

        forwards = []
        fip = self.find_or_create_floating_ip(parsed_args.external_ip_descriptor)
        internal_port = self.find_or_create_port(
            parsed_args.internal_ip_descriptor,
            internal_ip_network=parsed_args.internal_ip_network,
            internal_ip_subnet=parsed_args.internal_ip_subnet,
        )

        if isinstance(
            parsed_args.internal_ip_descriptor,
            (ipaddress.IPv4Address, ipaddress.IPv6Address),
        ):
            internal_ip_address = str(parsed_args.internal_ip_descriptor)
        else:
            # if we were given a port name, always pick the first fixed ip. if the user
            # wants to forward to a specific address, they should specify the address
            # rather than the port.
            internal_ip_address = internal_port.fixed_ips[0]["ip_address"]

        for port in parsed_args.port:
            if fwd := port_forwarding_exists(fip, internal_ip_address, port):
                forwards.append((fip, fwd))
            else:
                fwd = self.app.client_manager.sdk_connection.network.create_floating_ip_port_forwarding(
                    fip,
                    internal_ip_address=internal_ip_address,
                    internal_port=port.internal_port,
                    internal_port_id=internal_port.id,
                    external_port=port.external_port,
                    protocol=port.protocol,
                    **(
                        {"description": parsed_args.description}
                        if parsed_args.description
                        else {}
                    ),
                )
                forwards.append((fip, fwd))

        return forwards


class Delete(command.Lister, NetworkOpsMixin):
    """Delete a port forward from a floating ip to an internal address."""

    def get_parser(self, prog_name: str):
        parser = super().get_parser(prog_name)

        parser.add_argument("--port", "-p", type=PortSpec.from_spec, action="append")
        parser.add_argument(
            "internal_ip_descriptor",
            type=AddressOrPortArg(self),
            help="ip address, port name, or port uuid",
        )
        parser.add_argument(
            "external_ip_descriptor",
            type=ipaddress.ip_address,
            help="floating ip address",
        )

        return parser

    @format_forwards
    def take_action(self, parsed_args: argparse.Namespace):
        forwards = []

        fip = self.find_floating_ip(parsed_args.external_ip_descriptor)
        internal_port = self.find_port(parsed_args.internal_ip_descriptor)

        if isinstance(
            parsed_args.internal_ip_descriptor,
            (ipaddress.IPv4Address, ipaddress.IPv6Address),
        ):
            internal_ip_address = str(parsed_args.internal_ip_descriptor)
        else:
            # if we were given a port name, always pick the first fixed ip. if the user
            # wants to forward to a specific address, they should specify the address
            # rather than the port.
            internal_ip_address = internal_port.fixed_ips[0]["ip_address"]

        for port in parsed_args.port:
            for fwd in self.app.client_manager.sdk_connection.network.floating_ip_port_forwardings(
                fip
            ):
                if (
                    fwd.external_port == port.external_port
                    and fwd.internal_ip_address == internal_ip_address
                    and fwd.internal_port == port.internal_port
                ):
                    forwards.append((fip, fwd))
                    break
            else:
                raise KeyError(f"could not find port forwarding matching {port}")

        for fip, fwd in forwards:
            self.app.client_manager.sdk_connection.network.delete_floating_ip_port_forwarding(
                fip, fwd
            )

        return forwards


class Purge(command.Lister, NetworkOpsMixin):
    """Purge all port forwards associated with a floating ip address."""

    def get_parser(self, prog_name: str):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            "floating_ips",
            type=ipaddress.ip_address,
            nargs="+",
            help=_("List of floating ips from which to remove port forwardings"),
        )

        return parser

    @format_forwards
    def take_action(self, parsed_args: argparse.Namespace):
        forwards = []
        for ipaddr in parsed_args.floating_ips:
            fip = self.app.client_manager.sdk_connection.network.find_ip(str(ipaddr))
            forwards.extend(
                (fip, fwd)
                for fwd in self.app.client_manager.sdk_connection.network.floating_ip_port_forwardings(
                    fip
                )
            )

        for fip, fwd in forwards:
            self.app.client_manager.sdk_connection.network.delete_floating_ip_port_forwarding(
                fip, fwd
            )

        return forwards
