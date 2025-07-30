"""Contains player related classes."""

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


from typing import TypedDict, Optional, Union
from uuid import UUID

from pygame import Surface, Rect

from . import BaseSprite


type PlayerBounds = tuple[int, int, int, int]
type PlayerColor = tuple[int, int, int]
type PlayerPosition = tuple[float, float]
type PlayerSize = tuple[int, int]
type PlayerVelocity = tuple[float, float]


PLAYERS: dict[UUID, Union['MainPlayer', 'RemotePlayer']] = {}
PLAYER_SIZE: PlayerSize = (32, 32)


class PlayerAttributes(TypedDict):
    """A player's attributes."""

    color: PlayerColor
    position: PlayerPosition
    size: PlayerSize


class BasePlayer(BaseSprite):
    """Base player class."""

    def __init__(self, identity: UUID, bounds: PlayerBounds):
        """Args:
            identity:
                the UUID identifying the player.
            bounds:
                the area in which the player can move.
        """

        super().__init__()

        self._identity = identity

        self._surface = Surface((0, 0))
        self._surface.fill((0, 0, 0))
        self._rect = self._surface.get_rect()

        self._bounds = Rect(*bounds)

        self.__blit__ = [self._surface, self._rect]

    @property
    def surface(self) -> Surface:
        """The player surface."""

        return self._surface

    @property
    def rect(self) -> Rect:
        """The player rect."""

        return self._rect

    @property
    def x(self) -> float:
        """The x coordinate of the player."""

        return self._rect.x

    @property
    def y(self) -> float:
        """The y coordinate of the player."""

        return self._rect.y


class RemotePlayer(BasePlayer):
    """Represents a remote player."""

    def __init__(self, identity: UUID, bounds: PlayerBounds, color: PlayerColor, position: PlayerPosition, size: PlayerSize):
        """Args:
            identity:
                the UUID identifying the player.
            bounds:
                the area in which the player can move.
            color:
                the color of the player.
            position:
                the position of the player.
            size:
                the size of the player.
        """

        super().__init__(identity, bounds)

        self._position: PlayerPosition = position

        self._surface = Surface(size)
        self._surface.fill(color)
        self._rect = self._surface.get_rect()

        self.__blit__ = [self._surface, self._rect]

    def update(self, *args, **kwargs) -> None:
        """Updates the player's position."""

        super().update(*args, **kwargs)

        self._rect.move_ip(self._position[0] - self.x, self._position[1] - self.y)

    def set_position(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        """Sets the player's location."""

        if x is not None and y is not None:
            new_position = (x, y)
        elif x is not None:
            new_position = (x, self._position[1])
        elif y is not None:
            new_position = (self._position[0], y)
        else:
            new_position = self._position

        new_rect = Rect(*new_position, *self._surface.get_size())
        if self._bounds.contains(new_rect):
            for identity, player in PLAYERS.items():
                if identity == self._identity:
                    continue

                if new_rect.colliderect(player.rect):
                    break
            else:
                self._position = new_position


class MainPlayer(BasePlayer):
    """Represents the local player."""

    def __init__(self, identity: UUID, bounds: PlayerBounds, client):
        """Args:
            identity:
                the UUID identifying the player.
            bounds:
                the area in which the player can move.
            client:
                the TCP client used to communicate with the game server.
        """

        super().__init__(identity, bounds)

        self._client = client

        self._prev_position = (0.0, 0.0)
        self._velocity: PlayerVelocity = (0.0, 0.0)

    def update(self, *args, **kwargs) -> None:
        """Updates the player's position."""

        super().update(*args, **kwargs)

        new_rect = Rect(self.x + self._velocity[0], self.y + self._velocity[1], *self._surface.get_size())
        if self._bounds.contains(new_rect):
            for identity, player in PLAYERS.items():
                if identity == self._identity:
                    continue

                if new_rect.colliderect(player.rect):
                    break
            else:
                self._rect.move_ip(*self._velocity)

                if self._prev_position != (self.x, self.y):
                    self._client.update_position(self.x, self.y)

                    self._prev_position = (self.x, self.y)

    def set_attributes(self, attributes: PlayerAttributes) -> None:
        """Sets the player's attributes."""

        self._surface = Surface(attributes['size'])
        self._surface.fill(attributes['color'])

        self._rect = self._surface.get_rect()
        self._rect.update(*attributes['position'], *attributes['size'])
        self._prev_position = (self._rect.x, self._rect.y)

        self.__blit__ = [self._surface, self._rect]

    def set_velocity(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        """Sets the player's velocity."""

        if x is not None and y is not None:
            new_velocity = (x, y)
        elif x is not None:
            new_velocity = (x, self._velocity[1])
        elif y is not None:
            new_velocity = (self._velocity[0], y)
        else:
            new_velocity = self._velocity

        new_rect = Rect(self.x + new_velocity[0], self.y + new_velocity[1], *self._surface.get_size())
        if self._bounds.contains(new_rect):
            for identity, player in PLAYERS.items():
                if identity == self._identity:
                    continue

                if new_rect.colliderect(player.rect):
                    break
            else:
                self._velocity = new_velocity
