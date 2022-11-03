"""Wrapper for IGDB API."""
from __future__ import annotations

import time
import os
import typing

import httpx


class IGDB:
    """IGDB API methods."""

    def __init__(
        self,
        client_id: typing.Optional[str] = None,
        client_secret: typing.Optional[str] = None,
    ):
        """Initialise the class."""
        self._client = httpx.Client()
        self._client_id = client_id or os.environ.get("TWITCH_CLIENT_ID")
        self._client_secret = client_secret or os.environ.get("TWITCH_CLIENT_SECRET")

        if not self._client_id:
            raise ValueError("TWITCH_CLIENT_ID environment variable not set")

        if not self._client_secret:
            raise ValueError("TWITCH_CLIENT_SECRET environment variable not set")

    def __enter__(self) -> IGDB:
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exit the runtime context related to this object."""
        self._client.close()

    @property
    def _access_token_url(self) -> str:
        """Return the access token URL."""
        return (
            "https://id.twitch.tv/oauth2/"
            + f"token?client_id={self._client_id}&"
            + f"client_secret={self._client_secret}"
            + "&grant_type=client_credentials"
        )

    def get_access_token(self) -> str:
        """Get access token from Twitch API."""
        response = self._client.post(self._access_token_url)
        return response.json()["access_token"]

    def get_game_modes(self) -> list:
        """Get game modes from IGDB API."""
        headers = {
            "Client-ID": self._client_id,
            "Authorization": f"Bearer {self.get_access_token()}",
        }
        response = self._client.post(
            "https://api.igdb.com/v4/game_modes",
            headers=headers,
            data="fields *;",
        )
        return response.json()

    def get_games(
        self,
        exclude_ids: typing.List[int] = [],
        game_modes: typing.List[int] = [3],
    ) -> list:
        """Get up to 500 games from IGDB API."""
        headers = {
            "Client-ID": self._client_id,
            "Authorization": f"Bearer {self.get_access_token()}",
        }
        ids = {
            "" if not exclude_ids else f"& id != ({', '.join(map(str, exclude_ids))})"
        }
        response = self._client.post(
            "https://api.igdb.com/v4/games",
            headers=headers,
            data=f"""
                fields
                    name,
                    aggregated_rating,
                    rating,
                    first_release_date,
                    game_modes;
                where
                    rating != null
                    & aggregated_rating != null
                    & game_modes = {game_modes}
                    & category = 0
                    {ids};
                limit 500;
            """,
        )
        print(response.status_code)
        return response.json()

    def get_all_games(
        self,
        game_modes: typing.List[int] = [3],
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """Return all games from the IGDB API."""
        ids = []
        all_games = []
        while True:
            games = self.get_games(
                exclude_ids=ids,
                game_modes=game_modes,
            )
            print(f"Found {len(games)} games.")

            if not games:
                break

            all_games.extend(games)

            for game in games:
                ids.append(game["id"])

            time.sleep(0.25)

        return all_games
