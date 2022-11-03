"""IGDB API Client Library."""
from __future__ import annotations

__all__ = ("Game", "IGDB", "GAME_MODES")

from .igdb import IGDB
from .game import Game
from .game_modes import GAME_MODES
