"""Network utility functions."""

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


from ipaddress import IPv4Address, IPv6Address, ip_address
from socket import AF_INET, SOCK_DGRAM, socket


type NetworkAddress = tuple[IPv4Address | IPv6Address, int]


def get_local_ip() -> IPv4Address | IPv6Address:
    """Returns the IP address of the local machine."""

    with socket(AF_INET, SOCK_DGRAM) as s:
        s.connect(('1.1.1.1', 80))
        return ip_address(s.getsockname()[0])
