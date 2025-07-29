import csv
import logging

from parlaycooker.condition import is_valid_condition
from parlaycooker.model import Match

logger = logging.getLogger("csv_reader")


def read_matches_from_csv(filepath: str) -> tuple[list[Match], tuple[str, ...]]:
    """
    Reads matches and conditions from a CSV file.
    Assumes the file format has already been validated.
    """
    matches = []
    conditions = []

    logger.debug("Reading matches from CSV file: %s", filepath)

    # Validate the file format first
    validate_csv_format(filepath)

    with open(filepath, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if (
                not row
                or row[0].strip().startswith("#")
                or (not row[0].strip() and len(row) == 1)
            ):
                continue

            home_team, away_team, home, draw, away, condition = row

            match = Match(
                home_team=home_team.strip(),
                away_team=away_team.strip(),
                home=float(home),
                draw=float(draw),
                away=float(away),
            )
            matches.append(match)

            condition = condition.strip()
            if "*" in condition:
                condition = "HDA"

            conditions.append(condition)

    logger.debug("Total matches read: %d", len(matches))
    logger.debug("Total conditions read: %d", len(conditions))
    return matches, tuple(conditions)


def validate_csv_format(filepath: str) -> None:
    with open(filepath, mode="r") as file:
        reader = csv.reader(file)
        for row_number, row in enumerate(reader, start=1):
            if (
                not row
                or row[0].strip().startswith("#")
                or (not row[0].strip() and len(row) == 1)
            ):
                continue

            if len(row) != 6:
                raise ValueError(
                    f"Row {row_number} has an incorrect number of columns: {row}"
                )

            home_team, away_team, home, draw, away, condition = row

            if not (home_team and away_team and home and draw and away):
                raise ValueError(f"Row {row_number} has missing data: {row}")

            try:
                float(home)
                float(draw)
                float(away)
            except ValueError:
                raise ValueError(f"Row {row_number} contains invalid odds: {row}")

            if not is_valid_condition(condition.strip()):
                raise ValueError(
                    f"Row {row_number} contains an invalid condition: {condition}"
                )
