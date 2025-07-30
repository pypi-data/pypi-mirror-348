import logging
from vm_pkg_tools.utils.parser_utils import extract_section, parse_line
from vm_pkg_tools.validators.data_validator import validate_data


def extract_set_lines(content):
    """
    Extracts the lines from the [3SET] section.

    Args:
        content (str): The full scout file content.

    Returns:
        list: A list of lines within the [3SET] section.
    """
    try:
        return extract_section(content, "3SET").splitlines()
    except ValueError as e:
        logging.error(f"Error extracting [3SET] section: {e}")
        raise ValueError("[3SET] section not found.") from e


def parse_scores(score_data):
    """
    Parses individual score entries into home and away scores.

    Args:
        score_data (list): List of score strings.

    Returns:
        list: A list of dictionaries with home and away scores.
    """
    scores = []
    for score in score_data:
        try:
            home, away = map(int, score.strip().replace(" ", "").split("-"))
            scores.append({"home": home, "away": away})
        except ValueError:
            logging.warning(f"Invalid score format: {score}")
    return scores


def parse_final_scores_and_winner(final_score_data):
    """
    Parses the final scores and determines the set winner.

    Args:
        final_score_data (str): Final score string.

    Returns:
        dict: Parsed final scores and winner.
    """
    try:
        home_final, away_final = map(
            int, final_score_data.strip().replace(" ", "").split("-")
        )
        return {
            "final_scores": {"home": home_final, "away": away_final},
            "set_winner": "home" if home_final > away_final else "away",
        }
    except ValueError:
        logging.warning(f"Invalid final score format: {final_score_data}")
        return {"final_scores": None, "set_winner": None}


def parse_duration(duration_data):
    """
    Parses the duration of the set.

    Args:
        duration_data (str): Duration data string.

    Returns:
        int: Duration in minutes, or None if invalid.
    """
    if duration_data.strip().isdigit():
        return int(duration_data.strip())
    logging.warning(f"Invalid duration format: {duration_data}")
    return None


def parse_single_set(index, line):
    """
    Parses a single set entry.

    Args:
        index (int): Index of the set.
        line (str): Line containing set data.

    Returns:
        dict: Parsed set details.
    """
    set_data = parse_line(line, delimiter=";")
    set_number = index + 1

    scores = parse_scores(set_data[1:5])
    final_scores_and_winner = (
        parse_final_scores_and_winner(set_data[4]) if len(set_data) > 4 else {}
    )
    duration_minutes = parse_duration(set_data[5]) if len(set_data) > 5 else None

    parsed_set = {
        "set_number": set_number,
        "scores": scores,
        "set_winner": final_scores_and_winner.get("set_winner"),
        "final_scores": final_scores_and_winner.get("final_scores"),
        "duration_minutes": duration_minutes,
    }

    # Validate parsed set
    is_valid, validation_message = validate_data(parsed_set)
    if not is_valid:
        logging.error(f"Validation failed for set {set_number}: {validation_message}")
        return None

    return parsed_set


def parse_sets(content):
    """
    Parses all sets from the scout file content.

    Args:
        content (str): The full scout file content.

    Returns:
        list: A list of parsed sets.
    """
    try:
        lines = extract_set_lines(content)
        sets = []

        for i, line in enumerate(lines):
            logging.info(f"Parsing set line: {line}")
            if len(parse_line(line, delimiter=";")) < 5:
                logging.warning(f"Incomplete set data: {line}")
                continue

            set_data = parse_single_set(i, line)
            if set_data:
                sets.append(set_data)

        return sets
    except ValueError as e:
        logging.error(f"Error parsing sets: {e}")
        raise
