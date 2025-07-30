"""Contains all the server-side logic."""

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


from dataclasses import dataclass, field
import logging
from random import randint, random
from socket import AF_INET, error as socket_error, SOCK_STREAM, socket
import struct
from threading import Thread
from uuid import UUID, uuid4

from pygame import Rect

from .filters import PacketFilter, player_collision_filter, position_filter, whitelist_packets
from .packet import Packet, PacketType, EmbeddedPacket, LeavePacket, JoinPacket
from ..game.main import BOUNDS
from ..game.sprites.player import PLAYER_SIZE, PlayerAttributes, PlayerPosition

logger = logging.getLogger(__name__)


@dataclass
class TCPServer:
    """TCP server that functions as the game server."""

    _backlog: int = field(default_factory=lambda: 16, init=False)
    _connections: dict[socket, UUID] = field(default_factory=lambda: {}, init=False)
    _state: dict[UUID, PlayerAttributes] = field(default_factory=lambda: {}, init=False)
    address: (str, int)
    filters: list[PacketFilter] = field(
        default_factory=lambda: [
            player_collision_filter(),
            position_filter(0, 0, *BOUNDS),
            whitelist_packets(PacketType.POSITION),
        ],
    )

    def start(self) -> None:
        """Starts the server."""

        thread = Thread(target=TCPServer._handle_server, args=(self,))
        thread.start()

    def _forward_packet(self, source: socket, packet: Packet) -> None:
        for s in self._connections:
            if s != source:
                s.sendall(packet.to_bytes())

    def _init_player_attributes(self, identity: UUID) -> None:
        new_player_position: PlayerPosition = (0.0, 0.0)

        spawn_found: bool = False
        while not spawn_found:
            new_player_position = random() * (BOUNDS[0] - PLAYER_SIZE[0]), random() * (BOUNDS[1] - PLAYER_SIZE[1])
            new_player_rect = Rect(*new_player_position, *PLAYER_SIZE)

            for other_player in self._state.values():
                other_player_rect = Rect(*other_player['position'], *other_player['size'])

                if other_player_rect.colliderect(new_player_rect):
                    break
            else:
                spawn_found = True

        self._state[identity] = PlayerAttributes(**{
            'color': tuple(randint(64, 255) for _ in range(3)),
            'position': new_player_position,
            'size': PLAYER_SIZE,
        })

    def _handle_server(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind(self.address)
            s.listen(self._backlog)

            logger.info(
                'binding on address %s (%d).',
                '{}:{}'.format(*self.address), self._backlog
            )

            logging.info('game server started.')

            try:
                while True:
                    sock, addr = s.accept()
                    new_identity: UUID = uuid4()
                    self._connections[sock] = new_identity
                    logger.info(
                        'new connection from %s (%s).',
                        '{}:{}'.format(*addr), new_identity,
                    )

                    thread = Thread(target=TCPServer._handle_client, args=(self, sock))
                    thread.start()
            finally:
                logger.info('game server down.')

    def _handle_client(self, sock: socket) -> None:
        identity: UUID = self._connections[sock]

        logger.debug('player (%s) has joined the server.', identity)

        self._init_player_attributes(identity)
        join_packet = JoinPacket.from_attributes(self._state[identity])

        self._forward_packet(
            sock,
            EmbeddedPacket.from_packet(identity, join_packet),
        )

        sock.sendall(EmbeddedPacket.from_packet(UUID(int=0), join_packet).to_bytes())

        for other_identity, state in self._state.items():
            if other_identity != identity:
                join_packet = JoinPacket.from_attributes(state)
                sock.sendall(EmbeddedPacket.from_packet(other_identity, join_packet).to_bytes())

        try:
            while True:
                try:
                    packet = Packet.from_socket(sock).parse()
                except (struct.error, ValueError):
                    logger.warning('discarding malformed packet from (%s).', identity)
                    continue

                logger.debug('received packet from (%s) %r.', identity, packet)

                for packet_filter in self.filters:
                    if not packet_filter(identity, packet, self._state):
                        logger.debug('packet filtered (%s) %r.', identity, packet)

                        break
                else:
                    match packet.type:
                        case PacketType.POSITION:
                            logger.debug(
                                'update player (%s) position (%.2f, %.2f) -> (%.2f, %.2f).',
                                identity, *self._state[identity]['position'], packet.x, packet.y
                            )

                            self._state[identity]['position'] = (packet.x, packet.y)

                    self._forward_packet(
                        sock,
                        EmbeddedPacket.from_packet(identity, packet),
                    )

        except socket_error:
            self._forward_packet(
                sock,
                EmbeddedPacket.from_packet(identity, LeavePacket.new()),
            )

        finally:
            logger.info('connection closed (%d).', identity)

            self._connections.pop(sock)
            self._state.pop(identity)
            sock.close()

    def add_filter(self, packet_filter: PacketFilter) -> None:
        """Adds a packet filter to the server."""

        self.filters.append(packet_filter)
