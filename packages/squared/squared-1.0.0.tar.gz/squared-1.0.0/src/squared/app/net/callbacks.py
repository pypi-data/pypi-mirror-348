"""Contains client-side recv callbacks."""


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
from uuid import UUID

from .packet import Packet, JoinPacket, LeavePacket, PositionPacket
from ..game.sprites.player import PlayerAttributes, PlayerPosition


type ClientCallback = Callable[[UUID, Packet], Packet | None]


def on_player_join(action: Callable[[UUID, PlayerAttributes], None]) -> ClientCallback:
    """Returns a client callback that runs on player join.

    Args:
        action:
            the function to run on player join.
    """

    def callback(identity: UUID, packet: Packet) -> Packet | None:
        if not isinstance(packet, JoinPacket):
            return packet

        return action(identity, packet.attributes)

    return callback


def on_player_leave(action: Callable[[UUID], None]) -> ClientCallback:
    """Returns a client callback that runs on player leave.

    Args:
        action:
            the function to run on player leave.
    """

    def callback(identity: UUID, packet: Packet) -> Packet | None:
        if not isinstance(packet, LeavePacket):
            return packet

        return action(identity)

    return callback


def on_player_move(action: Callable[[UUID, PlayerPosition], None]) -> ClientCallback:
    """Returns a client callback that runs on player move.

    Args:
        action:
            the function to run on player move.
    """

    def callback(identity: UUID, packet: Packet) -> Packet | None:
        if not isinstance(packet, PositionPacket):
            return packet

        return action(identity, (packet.x, packet.y))

    return callback
