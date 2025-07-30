import logging


def create_set_details(set_id, points, lineups):
    logging.debug(f"Creating set details for set {set_id}.")
    logging.debug(f"Poins: {points}")
    logging.debug(f"Lineups: {lineups}")

    home_lineup = lineups.get("home", {})
    away_lineup = lineups.get("away", {})

    return {
        "set_id": set_id,
        "starting_lineups": {
            "home": {
                "setter_number": home_lineup.get("setter_number"),
                "setter_zone": home_lineup.get("setter_zone"),
                **{f"zone_{i}": home_lineup.get(f"zone_{i}") for i in range(1, 7)},
            },
            "away": {
                "setter_number": away_lineup.get("setter_number"),
                "setter_zone": away_lineup.get("setter_zone"),
                **{f"zone_{i}": away_lineup.get(f"zone_{i}") for i in range(1, 7)},
            },
        },
        "points": points,
    }


def parse_sets(content):
    """
    Parses set markers from the content.
    """
    set_markers = [
        line.strip()
        for line in content.splitlines()
        if line.startswith("**") and "set" in line
    ]
    logging.debug(f"Extracted set markers: {set_markers}")
    return set_markers
