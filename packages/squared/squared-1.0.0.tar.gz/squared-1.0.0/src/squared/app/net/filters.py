"""Contains server-side packet filters."""


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


from collections.abc import Callable
from typing import Optional
from uuid import UUID

from pygame import Rect

from ..game.sprites.player import PLAYER_SIZE, PlayerAttributes
from .packet import Packet, PacketType

type PacketFilter = Callable[[UUID, Packet, Optional[dict[UUID, PlayerAttributes]]], bool]


def whitelist_packets(*args: PacketType) -> PacketFilter:
    """Returns a packet filter that allows only certain packets to go through.

    Args:
        *args:
            a list of allowed packets.
    """

    def packet_filter(_identity: UUID, pkt: Packet, _state: Optional[dict[UUID, PlayerAttributes]] = None) -> bool:
        if pkt.type not in args:
            return False

        return True

    return packet_filter


def position_filter(left: int, top: int, w: int, h: int) -> PacketFilter:
    """Returns a packet filter that allows only position inside a certain perimeter.

    Args:
        left:
            the x coordinate of the top left corner of the perimeter.
        top:
            the y coordinate of the top left corner of the perimeter.
        w:
            the width of the perimeter.
        h:
            the height of the perimeter.
    """

    def packet_filter(_identity: UUID, pkt: Packet, _state: Optional[dict[UUID, PlayerAttributes]] = None) -> bool:
        if pkt.type != PacketType.POSITION:
            return True

        bounds = Rect(left, top, w, h)
        if bounds.contains(Rect(pkt.x, pkt.y, *PLAYER_SIZE)):
            return True

        return False

    return packet_filter


def player_collision_filter() -> PacketFilter:
    """Returns a packet filter that allows blocks position packets that would leed to overlapped players."""

    def packet_filter(identity: UUID, pkt: Packet, state: Optional[dict[UUID, PlayerAttributes]] = None) -> bool:
        if pkt.type != PacketType.POSITION:
            return True

        if not state:
            return True

        if not (this_player_attributes := state.get(identity, None)):
            return False
        this_player_new_rect = Rect(pkt.x, pkt.y, *this_player_attributes['size'])

        for other_player_identity, other_player_attributes in state.items():
            if identity == other_player_identity:
                continue

            other_player_rect = Rect(*other_player_attributes['position'], *other_player_attributes['size'])
            if this_player_new_rect.colliderect(other_player_rect):
                break
        else:
            return True

        return False

    return packet_filter
