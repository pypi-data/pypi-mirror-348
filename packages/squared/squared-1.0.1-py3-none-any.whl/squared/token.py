"""Handles server token generation and encoding."""

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


from base64 import urlsafe_b64decode, urlsafe_b64encode
from ipaddress import IPv4Address, IPv6Address, ip_address
import struct
from typing import Optional

from .modules.network import NetworkAddress



def stoken_encode(ip: IPv4Address | IPv6Address, port: int, default_port: Optional[int] = None) -> str:
    """Generates a server token given a network address.

    If a default port is specified, it will be omitted from the token.
    """

    blob: bytes = (
        struct.pack('>I', int(ip))
        if isinstance(ip, IPv4Address) else
        int(ip).to_bytes(16, byteorder='big')
    )

    if port != default_port:
        blob += struct.pack('>H', port)

    return urlsafe_b64encode(blob).decode().rstrip('=')


def stoken_decode(token: str, default_port: int) -> NetworkAddress:
    """Extracts the server ip and port from a server token.

    Raises:
        ValueError:
            the token is invalid.
    """

    blob: bytes = urlsafe_b64decode(token + '=' * (4 - len(token) % 4))

    match len(blob):
        case 4:   # IPv4.
            ip, port = *struct.unpack('>I', blob), default_port
        case 6:   # IPv4 + port.
            ip, port = struct.unpack('>IH', blob)
        case 16:  # IPv6.
            ip, port = int.from_bytes(blob[:16], byteorder='big'), default_port
        case 18:  # IPv6 + port.
            ip, port = int.from_bytes(blob[:16], byteorder='big'), *struct.unpack('>H', blob[-2:])
        case _:
            raise ValueError('invalid token')

    return ip_address(ip), port
