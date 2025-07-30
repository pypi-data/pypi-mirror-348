import logging
from vm_pkg_tools.parsers.match_actions.points_parser import parse_point
from vm_pkg_tools.parsers.match_actions.set_parser import create_set_details
from vm_pkg_tools.utils.parser_utils import find_set_number


def parse_match_actions(content, lineups):
    """
    Parses match actions for each set and correctly groups points by set using find_set_number.
    """
    points_lines = [
        line.strip() for line in content.splitlines() if line.startswith(("*p", "ap"))
    ]
    logging.debug(f"Extracted points lines: {points_lines}")

    set_markers = [
        line.strip()
        for line in content.splitlines()
        if line.startswith("**") and "set" in line
    ]
    logging.debug(f"Extracted set markers: {set_markers}")

    if not set_markers:
        logging.warning("No set markers found in content.")
        return []

    sets = []
    for idx, set_marker in enumerate(set_markers, start=1):
        logging.debug(f"Processing set {idx}: {set_marker}")

        # Filter points belonging to the current set
        set_points = []
        point_counter = 0  # Initialize point counter for this set
        for point_line in points_lines:
            set_number = find_set_number(point_line)
            if set_number == idx:
                point_idx = content.splitlines().index(point_line)
                next_point = (
                    points_lines[points_lines.index(point_line) + 1]
                    if points_lines.index(point_line) + 1 < len(points_lines)
                    else None
                )
                parsed_point = parse_point(
                    point_line,
                    content=content,
                    point_idx=point_idx,
                    next_point=next_point,
                    point_counter=point_counter,
                )
                if parsed_point:
                    set_points.append(parsed_point)
                    point_counter += 1  # Increment point counter after each point

        logging.debug(f"Points extracted for set {idx}: {set_points}")

        if not set_points:
            logging.warning(f"No points found for set {idx}.")

        # Create set details
        set_details = create_set_details(idx, set_points, lineups)
        logging.debug(f"Set {idx} details: {set_details}")
        sets.append(set_details)

    return sets
