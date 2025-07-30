import logging
from vm_pkg_tools.utils.parser_utils import extract_section, parse_line
from vm_pkg_tools.validators.data_validator import validate_data


def parse_teams(content):
    team_section = extract_section(content, "3TEAMS")
    lines = team_section.splitlines()

    teams = {"home": {}, "away": {}}
    for i, line in enumerate(lines[:2]):
        fields = parse_line(line, delimiter=";")
        if len(fields) < 3 or not fields[0].isdigit():
            logging.warning(f"Skipping invalid team line: {line}")
            continue

        try:
            team_data = {
                "id": int(fields[0]),
                "name": fields[1] or "Unknown Team",
                "sets_won": int(fields[2]) if fields[2].isdigit() else 0,
            }

            is_valid, validation_message = validate_data(team_data)
            if not is_valid:
                logging.warning(
                    f"Validation failed for team line: {line} - {validation_message}"
                )
                continue

            teams["home" if i == 0 else "away"] = team_data
        except ValueError as e:
            logging.error(f"Error parsing team line: {line} - {e}")

    return teams
