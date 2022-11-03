"""Get games from IGDB API and save them to a CSV file."""
from __future__ import annotations

import csv

from IGDB import IGDB, Game


def main():
    """Entry point."""
    with IGDB() as client:
        games = client.get_all_games()

        with open("games.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(
                Game.to_csv_header(),
            )

            for game in games:
                game = Game.from_dict(game)
                writer.writerow(
                    game.to_list(),
                )


if __name__ == "__main__":
    main()
