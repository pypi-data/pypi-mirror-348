"""Command Line Interface entry point."""

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


from argparse import Namespace
import logging

from .app.net.client import TCPClient
from .app.net.server import TCPServer
from .app.game import main as game
from .token import stoken_encode


logger = logging.getLogger(__name__)


def main(namespace: Namespace) -> None:
    """Main CLI function.

    Args:
        namespace:
          Namespace containing the command line parsing.
    """


    if namespace.connect:
        server_address = str(namespace.connect[0]), namespace.connect[1]

        game_client = TCPClient(server_address)
        game.run(game_client)

    if namespace.host:
        print(f'SERVER TOKEN: {stoken_encode(namespace.host[0], namespace.host[1], default_port=7173)}.')

        server_address = str(namespace.host[0]), namespace.host[1]

        game_server = TCPServer(server_address)
        game_server.start()
    elif namespace.connect:
        server_address = str(namespace.connect[0]), namespace.connect[1]

    game_client = TCPClient(server_address)
    game.run(game_client)
