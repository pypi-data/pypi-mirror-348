"""Contains all the client-side logic."""

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
from queue import Queue
from socket import AF_INET, SOCK_STREAM, socket
import struct
from threading import Thread
from uuid import UUID

from .callbacks import ClientCallback
from .packet import Packet, EmbeddedPacket, PositionPacket


logger = logging.getLogger(__name__)


@dataclass
class TCPClient:
    """TCP client used to communicate with the game server."""

    _outbound_packets_queue: Queue = field(init=False, default=Queue())
    address: tuple[str, int]
    callbacks: list[ClientCallback] = field(default_factory=lambda: [])

    def start(self) -> None:
        """Starts the client."""

        thread = Thread(target=TCPClient._handle_client, args=(self,))
        thread.start()

    def send_packet(self, packet: Packet) -> None:
        """Sends a packet to the game server.

        Args:
            packet:
                the packet to send.
        """

        self._outbound_packets_queue.put(packet)

    def update_position(self, x: int, y: int) -> None:
        """Updates the local player's position.

        Args:
            x:
                the x coordinate of the player.
            y:
                the y coordinate of the player.
        """

        self.send_packet(PositionPacket.from_coordinates(x, y))

    def _handle_client(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect(self.address)

            thread = Thread(target=TCPClient._handle_outbound_packets, args=(self, s))
            thread.start()

            self._handle_inbound_packets(s)

    def _handle_inbound_packets(self, sock: socket) -> None:
        try:
            while True:
                try:
                    packet = Packet.from_socket(sock).parse()
                except (struct.error, ValueError):
                    logger.warning('discarding malformed packet.')

                    continue

                if not isinstance(packet, EmbeddedPacket):
                    continue

                source_identity: UUID = packet.identity

                try:
                    packet: Packet = packet.embed.parse()
                except (struct.error, ValueError):
                    logger.warning('discarding malformed packet from (%s).', source_identity)

                    continue

                logger.debug('received packet from (%s) %r.', source_identity, packet)

                for callback in self.callbacks:
                    if (packet := callback(source_identity, packet)) is None:
                        break

        finally:
            logger.info('connection closed.')
            sock.close()

    def _handle_outbound_packets(self, sock: socket) -> None:
        while True:
            outbound_pkt: Packet = self._outbound_packets_queue.get()

            logger.debug('sent packet %r.', outbound_pkt)

            sock.sendall(outbound_pkt.to_bytes())

    def add_callback(self, callback: ClientCallback) -> None:
        """Adds a callback function to the client.

        Args:
            callback:
                the callback function to add.
        """

        self.callbacks.append(callback)

    def remove_callback(self, callback: ClientCallback) -> None:
        """Removes a callback function from the client.

        Args:
            callback:
                the callback function to remove.
        """

        self.callbacks.remove(callback)
