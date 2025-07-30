import logging
from vm_pkg_tools.utils.parser_utils import extract_section, parse_line
from vm_pkg_tools.validators.data_validator import validate_data


def parse_players(content, team_type):
    section_name = "3PLAYERS-H" if team_type == "home" else "3PLAYERS-V"
    lines = extract_section(content, section_name).splitlines()

    players = []
    for line in lines:
        fields = parse_line(line, delimiter=";")
        if len(fields) < 9:
            logging.warning(f"Skipping invalid player line: {line}")
            continue

        player_data = {
            "id": int(fields[8]) if fields[8].isdigit() else None,
            "jersey_number": int(fields[1]) if fields[1].isdigit() else None,
            "match_entry_number": int(fields[2]) if fields[2].isdigit() else None,
            "last_name": fields[9].strip(),
            "first_name": fields[10].strip(),
            "role": fields[12].strip().upper() if fields[12].strip() else None,
        }

        is_valid, validation_message = validate_data(player_data)
        if not is_valid:
            logging.warning(
                f"Validation failed for player line: {line} - {validation_message}"
            )
            continue

        players.append(player_data)
    return players
