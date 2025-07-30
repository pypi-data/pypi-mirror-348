"""Contains custom argparse types."""

# Copyright (C) 2025  Stefano Cuizza

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Optional

from ..lazy import LazyDict
from ..modules.network import get_local_ip, NetworkAddress
from ..token import stoken_decode


def network_port(argument: str) -> int:
    """Checks whether the provided argument is a valid port number."""

    if 0 < (port := int(argument)) <= 65535:
        return port

    raise ValueError(f'{port!r} is not in range (0, 65535]')


def network_ip(argument: str) -> IPv4Address | IPv6Address:
    """Checks whether the provided argument is a valid IP address.

    Some string constants are accepted and will be converted using the following
    conversion table:

    .. table:: Supported constants
        :widths: auto

        =========  ================
        constant   address
        =========  ================
           all         0.0.0.0
           lan     local ip address
        localhost     127.0.0.1
        =========  ================
    """

    conversion_table: LazyDict = LazyDict({
        'all': (lambda c: c, '0.0.0.0'),
        'lan': (lambda _: get_local_ip(), None),
        'localhost': (lambda c: c, '127.0.0.1'),
    })

    return ip_address(conversion_table.get(argument, argument))


def network_address(argument: str) -> NetworkAddress:
    """Checks whether the provided argument is a valid network address (ip:port)."""

    ip, port = argument.split(':', maxsplit=1)
    return network_ip(ip), network_port(port)


def network_address_with_optional_port(argument: str, port: Optional[int] = None) -> NetworkAddress:
    """Checks whether the provided argument is a valid network address (ip[:port])."""

    if not port or ':' in argument:
        return network_address(f'{argument}')

    return network_address(':'.join((argument, str(port))))


def server_token(argument: str, default_port: int) -> NetworkAddress:
    """Checks whether the provided argument is a valid server token.

    Server tokens provide an easy way to connect to a game server. A server
    token is just the game server ip + port encoded using base64.
    """

    return stoken_decode(argument, default_port)


def connection_address(argument: str, default_port: int) -> NetworkAddress:
    """Checks whether the provided argument is a valid connection address (ip[:port] | token)."""

    try:
        return network_address_with_optional_port(argument, default_port)
    except ValueError:
        pass

    return server_token(argument, default_port)
