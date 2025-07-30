"""Contains "lazy" implementations of built-in data types."""

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


from collections.abc import Mapping


# Guangyang Li (November 9 2017). Set up a dictionary lazily. Stackoverflow.
# https://stackoverflow.com/a/47212782.
class LazyDict(Mapping):
    """Lazy implementation of dict."""

    def __init__(self, *args, **kw):
        self._data = dict(*args, **kw)

    def __getitem__(self, key):
        func, arg = self._data.__getitem__(key)
        return func(arg)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)
