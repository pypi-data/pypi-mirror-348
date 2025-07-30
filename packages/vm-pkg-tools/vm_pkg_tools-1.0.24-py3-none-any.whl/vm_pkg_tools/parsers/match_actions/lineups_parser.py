import logging
from vm_pkg_tools.utils.parser_utils import extract_section


def parse_setter_details(lines, setter_type):
    """Extract setter number and zone details."""
    try:
        logging.debug(f"Looking for setter details in lines for type: {setter_type}.")
        setter_number_line = next(
            (line for line in lines if setter_type + "P" in line), None
        )
        setter_zone_line = next(
            (line for line in lines if setter_type + "z" in line), None
        )

        if not setter_number_line or not setter_zone_line:
            logging.warning(f"No setter details found for {setter_type}.")
            return {"setter_number": None, "setter_zone": None}

        setter_number = int(setter_number_line.split(">")[0][2:4])
        setter_zone = int(setter_zone_line.split(">")[0][2])
        return {"setter_number": setter_number, "setter_zone": setter_zone}
    except ValueError as e:
        logging.error(f"Error extracting setter details for {setter_type}: {e}")
        return {"setter_number": None, "setter_zone": None}


def extract_zone_from_lines(lines):
    """Extract starting lineup zones for both home and away teams."""
    home_zones = {f"zone_{i}": None for i in range(1, 7)}
    away_zones = {f"zone_{i}": None for i in range(1, 7)}

    for line in lines:
        if "LUp" in line:
            try:
                logging.debug(f"Processing lineup line: {line}")
                components = line.split(";")[::-1]

                new_list = []
                empty_count = 0

                for item in components:
                    if item == "":
                        empty_count += 1
                        if empty_count == 2:
                            break
                    else:
                        empty_count = 0
                        if item.isdigit():
                            new_list.append(int(item))

                lineup_players = new_list[::-1]

                if len(lineup_players) >= 12:
                    for i in range(6):
                        home_zones[f"zone_{i + 1}"] = lineup_players[i]
                        away_zones[f"zone_{i + 1}"] = lineup_players[i + 6]
                    logging.info(f"Extracted home zones: {home_zones}")
                    logging.info(f"Extracted away zones: {away_zones}")
                    return {"home": home_zones, "away": away_zones}
                else:
                    logging.warning(f"Insufficient numbers for lineup in line: {line}")
            except ValueError as e:
                logging.error(f"Error parsing lineup numbers in line: {line} - {e}")
    logging.warning("No valid lineup found.")
    return {"home": home_zones, "away": away_zones}


def parse_team_lineups(lines, lineup_type):
    """Parse the team lineups."""
    logging.info(f"Parsing team lineups for type: {lineup_type}.")
    setter_details = parse_setter_details(lines, "*" if lineup_type == "home" else "a")
    zones = extract_zone_from_lines(lines)
    team_lineup = {**setter_details, **zones[lineup_type]}
    logging.debug(f"Parsed lineup for {lineup_type}: {team_lineup}")
    return team_lineup


def parse_lineups(content):
    """Parse lineups from the [3SCOUT] section."""
    try:
        logging.info("Parsing [3SCOUT] section for lineups.")
        scout_section = extract_section(content, "3SCOUT")
        if not scout_section:
            logging.warning("[3SCOUT] section is missing or empty.")
            return {"home": {}, "away": {}}

        lines = scout_section.splitlines()
        home_lines = [line for line in lines if line.startswith("*")]
        away_lines = [line for line in lines if line.startswith("a")]

        # Debugging lineup type
        logging.debug(f"Home lines: {home_lines}")
        logging.debug(f"Away lines: {away_lines}")

        parsed_lineups = {
            "home": parse_team_lineups(home_lines, "home"),
            "away": parse_team_lineups(away_lines, "away"),
        }
        logging.info(f"Parsed lineups: {parsed_lineups}")
        return parsed_lineups
    except ValueError as e:
        logging.error(f"Error parsing lineups: {e}")
        return {
            "home": {
                "setter_number": None,
                "setter_zone": None,
                **{f"zone_{i}": None for i in range(1, 7)},
            },
            "away": {
                "setter_number": None,
                "setter_zone": None,
                **{f"zone_{i}": None for i in range(1, 7)},
            },
        }
