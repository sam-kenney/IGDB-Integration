"""Class representing a Game."""
from __future__ import annotations

import typing

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Game:
    """Represent a game."""

    name: str
    rating: float
    aggregated_rating: float
    release_date: str
    is_singleplayer: bool
    is_multiplayer: bool
    is_cooperative: bool
    is_splitscreen: bool
    is_mmo: bool
    is_battle_royale: bool

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> Game:
        """Construct a Game from a dict."""
        release_date = datetime.fromtimestamp(data["first_release_date"]).strftime(
            "%Y-%m-%d"
        )

        return cls(
            name=data["name"],
            rating=data["rating"],
            aggregated_rating=data["aggregated_rating"],
            release_date=release_date,
            is_singleplayer=1 in data["game_modes"],
            is_multiplayer=2 in data["game_modes"],
            is_cooperative=3 in data["game_modes"],
            is_splitscreen=4 in data["game_modes"],
            is_mmo=5 in data["game_modes"],
            is_battle_royale=6 in data["game_modes"],
        )

    def to_list(self) -> typing.List[str | bool | float]:
        """Return the game as a csv compatible list."""
        return [
            self.name,
            self.rating,
            self.aggregated_rating,
            self.release_date,
            self.is_singleplayer,
            self.is_multiplayer,
            self.is_cooperative,
            self.is_splitscreen,
            self.is_mmo,
            self.is_battle_royale,
        ]

    @staticmethod
    def to_csv_header() -> typing.List[str]:
        """Return the csv header."""
        return [
            "name",
            "rating",
            "aggregated_rating",
            "release_date",
            "is_singleplayer",
            "is_multiplayer",
            "is_cooperative",
            "is_splitscreen",
            "is_mmo",
            "is_battle_royale",
        ]
