"""Contains the packet definitions used by the game alongside some helper functions."""

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


from enum import auto, IntEnum
from socket import error as socket_error, socket
import struct
from typing import Self
from uuid import UUID

from ..game.sprites.player import PlayerAttributes


class PacketType(IntEnum):
    """Enum containing all possible packet types."""

    EMBEDDED = auto()
    JOIN = auto()
    LEAVE = auto()
    POSITION = auto()


class Packet:
    """A generic packet."""

    def __init__(self, type: PacketType, length: int, data: bytes):
        """Args:
            type:
                the packet type
            length:
                the length of the packet's data.
            data:
                 the packet's data.
        """

        if (actual_length := len(data)) != length:
            raise ValueError(
                f'packet length mismatch ({length} != {actual_length})'
            )

        self._type: PacketType = type
        self._length: int = length
        self._data: bytes = data

    @classmethod
    def from_socket(cls, stream: socket):
        """Builds a packet by reading a socket."""

        blob: bytes = stream.recv(2)
        if not blob:
            raise socket_error

        packet_type = PacketType.from_bytes(blob, byteorder='big')

        blob: bytes = stream.recv(4)
        if not blob:
            raise socket_error

        packet_length: int = struct.unpack('>I', blob)[0]

        packet_data = stream.recv(packet_length)
        if not packet_data or len(packet_data) != packet_length:
            raise socket_error

        return cls(packet_type, packet_length, packet_data)

    @classmethod
    def from_bytes(cls, bytes: bytes):
        """Builds a packet by reading a bytearray."""

        if len(bytes) < 6:
            raise ValueError('packet too short')

        packet_type = PacketType.from_bytes(bytes[:2], byteorder='big')
        packet_length: int = struct.unpack('>I', bytes[2:6])[0]
        packet_data = bytes[6:]

        return cls(packet_type, packet_length, packet_data)

    def to_bytes(self) -> bytes:
        """Serializes a packet to bytes."""

        return (
            self.type.to_bytes(2, byteorder='big') +
            self.length.to_bytes(4, byteorder='big') +
            self.data
        )

    def parse(self) -> Self:
        """Parse a generic packet into a specific type."""

        match self.type:
            case PacketType.EMBEDDED:
                con = EmbeddedPacket
            case PacketType.JOIN:
                con = JoinPacket
            case PacketType.LEAVE:
                con = LeavePacket
            case PacketType.POSITION:
                con = PositionPacket
            case _:
                con = Packet

        return con(self.type, self.length, self.data)

    @property
    def type(self) -> PacketType:
        """The packet type."""

        return self._type

    @property
    def length(self) -> int:
        """The packet's data length."""

        return self._length

    @property
    def data(self) -> bytes:
        """Tha packet's data."""

        return self._data

    def __repr__(self):
        return f'Packet(type={self.type.name}, length={self.length}, data={self.data})'


class EmbeddedPacket(Packet):
    """A packet that contains another packet with an assigned identity."""

    def __init__(self, *args, **kwargs):
        """"""

        super().__init__(*args, **kwargs)

        self._id, self._embedded_packet = (
            UUID(int=int.from_bytes(self.data[:16], byteorder='big')),
            Packet.from_bytes(self.data[16:]),
        )

    @classmethod
    def from_packet(cls, identity: UUID, packet: Packet):
        """Creates a new embedded packet from a packet.

        Args:
            identity:
                the identity of the packet.
            packet:
                the packet to create the embedded packet from.
        """

        packet_data: bytes = (
                int(identity).to_bytes(16, byteorder='big') +
                packet.to_bytes()
        )

        return cls(PacketType.EMBEDDED, len(packet_data), packet_data)

    @property
    def identity(self) -> UUID:
        """The packet's identity."""

        return self._id

    @property
    def embed(self) -> Packet:
        """The embedded packet."""

        return self._embedded_packet


class JoinPacket(Packet):
    """A packet that signals a player joining the server."""

    def __init__(self, *args, **kwargs):
        """"""

        super().__init__(*args, **kwargs)

        r, g, b, x, y, width, height = struct.unpack('>3B2f2B', self.data[:13])

        self._attributes: PlayerAttributes = {
            'color': (r, g, b),
            'position': (x, y),
            'size': (width, height),
        }

    @classmethod
    def from_attributes(cls, attributes: PlayerAttributes):
        """Creates a new join packet from a player's attributes."""

        packet_data: bytes = (
            struct.pack('>3B', *attributes['color']) +
            struct.pack('>2f', *attributes['position']) +
            struct.pack('>2B', *attributes['size'])
        )

        return cls(PacketType.JOIN, len(packet_data), packet_data)

    @property
    def attributes(self) -> PlayerAttributes:
        """The new player's attributes."""

        return self._attributes


class LeavePacket(Packet):
    """A packet that signals a player leaving the server."""

    @classmethod
    def new(cls):
        """Creates a new leave packet."""

        return cls(PacketType.LEAVE, 0, b'')


class PositionPacket(Packet):
    """A packet that contains a player's position."""

    def __init__(self, *args, **kwargs):
        """"""

        super().__init__(*args, **kwargs)

        self._x, self._y = struct.unpack('>2f', self.data)

    @classmethod
    def from_coordinates(cls, x: float, y: float):
        """Creates a new position packet given a pair of coordinates."""

        return cls(PacketType.POSITION, 8, struct.pack('>2f', x, y))

    @property
    def x(self) -> float:
        """The x coordinate contained inside the packet."""

        return self._x

    @property
    def y(self) -> float:
        """The y coordinate contained inside the packet."""

        return self._y
