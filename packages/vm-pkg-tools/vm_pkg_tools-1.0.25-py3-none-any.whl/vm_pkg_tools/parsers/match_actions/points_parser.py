import logging
from vm_pkg_tools.utils.parser_utils import (
    is_valid_action_line,
    parse_action_line,
    extract_timestamp,
)


def extract_rally_winner(line: str) -> str | None:
    """
    Determine the rally winner from the line.
    """
    return (
        "home" if line.startswith("*p") else "away" if line.startswith("ap") else None
    )


def extract_point_identifier(line: str) -> str | None:
    """
    Extract the point identifier from the line.
    """
    return line.split(";", 1)[0].strip()


def extract_actions(
    content: str, point_idx: int, next_point: str | None = None
) -> list[dict]:
    """
    Extract actions between points.
    """
    lines = content.splitlines()
    actions = []

    # Find the last action index for this rally (before the point line)
    last_action_of_rally_idx = point_idx - 1
    if next_point:
        try:
            next_point_idx = lines.index(next_point)
            last_action_of_rally_idx = min(last_action_of_rally_idx, next_point_idx - 1)
        except ValueError:
            logging.warning(f"Next point {next_point} not found. Using default range.")

    if last_action_of_rally_idx < 0 or last_action_of_rally_idx >= len(lines):
        logging.error(
            f"last_action_of_rally_idx out of bounds: {last_action_of_rally_idx}"
        )
        return []

    # Backtrack to find the service action (first action of the rally)
    first_action_of_rally_idx = last_action_of_rally_idx
    while first_action_of_rally_idx > 0:
        line = lines[first_action_of_rally_idx].strip()
        if (
            is_valid_action_line(line) and line[3] == "S"
        ):  # Check if it's a service action
            break
        first_action_of_rally_idx -= 1

    # Start collecting actions from service to the point
    action_id = 1  # Start with action_id 1 for each point
    for i in range(first_action_of_rally_idx, last_action_of_rally_idx + 1):
        parsed_action = parse_action_line(lines[i].strip())
        if parsed_action:
            parsed_action["action_id"] = action_id
            actions.append(parsed_action)
            action_id += 1  # Increment action_id for next action

    logging.debug(f"Extracted actions: {actions}")
    return actions


def parse_point(
    line: str,
    content: str,
    point_idx: int,
    next_point: str | None = None,
    point_counter: int = 0,
) -> dict | None:
    """
    Parse a point line and associated actions into a structured dictionary.
    """
    try:
        parts = line.split(";")
        if len(parts) < 2:
            logging.warning(f"Point line is too short: {line}")
            return None

        # Extract point-level information
        point = extract_point_identifier(line)
        rally_winner = extract_rally_winner(line)
        local_timestamp = extract_timestamp(parts)

        # Extract associated actions
        actions = extract_actions(content, point_idx, next_point)

        if not point or not local_timestamp:
            logging.warning(f"Point or timestamp missing for line: {line}")
            return None

        # Increment point_id for each point
        point_id = point_counter + 1

        return {
            "point_id": point_id,
            "point": point,
            "rally_winner": rally_winner,
            "local_timestamp": local_timestamp,
            "video_timestamp": "",
            "actions": actions,
        }
    except Exception as e:
        logging.error(f"Error parsing point line: {line} - {e}")
        return None
