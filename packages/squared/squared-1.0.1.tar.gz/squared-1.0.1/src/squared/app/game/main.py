"""Main game file."""

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


import logging
from typing import Final
from uuid import UUID

import pygame
from pygame import Surface

from ...modules import metadata
from ..net.client import TCPClient
from ..net.callbacks import on_player_join, on_player_leave, on_player_move
from .sprites.player import MainPlayer, PLAYERS, PlayerAttributes, PlayerPosition, RemotePlayer


logger = logging.getLogger(__name__)

BOUNDS: Final[tuple[int, int]] = (720, 480)


def get_main_player() -> MainPlayer:
    """Returns the local player."""

    return PLAYERS[UUID(int=0)]


def on_player_join_action(identity: UUID, attributes: PlayerAttributes) -> None:
    """Function that gets called on player join."""

    if int(identity) == 0:
        PLAYERS[identity].set_attributes(attributes)
    else:
        PLAYERS[identity] = RemotePlayer(identity, (0, 0, *BOUNDS), **attributes)


def on_player_leave_action(identity: UUID) -> None:
    """Function that gets called on player leave."""

    if int(identity) == 0:
        return

    PLAYERS.pop(identity, None)


def on_player_move_action(identity: UUID, position: PlayerPosition) -> None:
    """Function that gets called on player move."""

    if int(identity) == 0:
        return

    if player := PLAYERS.get(identity):
        player.set_position(*position)


def init(title: str, size: tuple[int, int]) -> Surface:
    """Initializes the game."""

    successes, failures = pygame.init()

    logger.debug(
        'initializing pygame: %d successes and %d failures.',
        successes, failures
    )

    pygame.display.set_caption(title)
    return pygame.display.set_mode(size)


def main(screen: Surface, fps: int) -> None:
    """Starts the game."""

    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(fps) / 1000

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    get_main_player().set_velocity(y=-200 * dt)
                elif event.key == pygame.K_s:
                    get_main_player().set_velocity(y=200 * dt)
                elif event.key == pygame.K_a:
                    get_main_player().set_velocity(x=-200 * dt)
                elif event.key == pygame.K_d:
                    get_main_player().set_velocity(x=200 * dt)

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    get_main_player().set_velocity(y=0)
                elif event.key in (pygame.K_a, pygame.K_d):
                    get_main_player().set_velocity(x=0)

        for p in PLAYERS.values():
            p.update()
            screen.blit(*p.__blit__)

        pygame.display.update()


def run(client: TCPClient) -> None:
    """Runs the game.

    Args:
        client:
            the TCP client used to communicate with the game server.
    """

    PLAYERS[UUID(int=0)] = MainPlayer(UUID(int=0), (0, 0, *BOUNDS), client)

    client.add_callback(on_player_join(on_player_join_action))
    client.add_callback(on_player_leave(on_player_leave_action))
    client.add_callback(on_player_move(on_player_move_action))

    client.start()

    window_title: str = f'{metadata.package().capitalize()} - v{metadata.version()}'
    screen = init(window_title, BOUNDS)

    main(screen, 60)
