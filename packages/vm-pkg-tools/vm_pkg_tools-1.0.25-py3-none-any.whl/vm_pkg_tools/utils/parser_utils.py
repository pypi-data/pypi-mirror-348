import re
import logging

# Constants
SKILL_DICT = {
    "S": "service",
    "R": "reception",
    "A": "attack",
    "B": "block",
    "D": "dig",
    "E": "set",
    "F": "free-ball",
    "&": "default_skill",
}

SKILL_TYPE_DICT = {
    "H": "high",
    "M": "medium",
    "T": "tense",
    "Q": "quick",
    "U": "super",
    "F": "fast",
    "O": "other",
}

RESULT_ACTION_DICT = {
    "#": "double-plus",
    "+": "plus",
    "!": "exclamation",
    "/": "slash",
    "-": "minus",
    "=": "double-minus",
}


def extract_section(content: str, section_name: str) -> str:
    """
    Extracts a specific section from the given content based on the section name.

    Args:
        content (str): The full text content.
        section_name (str): The name of the section to extract.

    Returns:
        str: The content of the specified section.
    """
    pattern = rf"\[{section_name}](.*?)(\[|$)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        section = match.group(1).strip()
        logging.debug(f"Extracted section [{section_name}]: {section[:100]}...")
        return section
    logging.warning(f"Section [{section_name}] not found in content.")
    return ""


def parse_line(line: str, delimiter: str = ";", log: bool = False) -> list:
    """
    Parses a single line of text into fields based on a delimiter.

    Args:
        line (str): The line to parse.
        delimiter (str): The delimiter to split the line.
        log (bool): Whether to log the parsed line.

    Returns:
        list: A list of fields extracted from the line.
    """
    fields = [field.strip() for field in line.split(delimiter)]
    if log:
        logging.debug(f"Parsed line: {line} -> {fields}")
    return fields


def find_set_number(line: str) -> int | None:
    """
    Detects and extracts the set number from a given line.

    Args:
        line (str): A line of text to search for a set number.

    Returns:
        int or None: The extracted set number, or None if not found.
    """
    pattern = re.compile(r";(\d+);")
    match = pattern.search(line.strip())
    if match:
        set_number = int(match.group(1))
        logging.debug(f"Found set number in line '{line}': {set_number}")
        return set_number
    logging.debug(f"No set number found in line: {line}")
    return None


def extract_numeric_fields(fields: list) -> list:
    """
    Converts a list of strings to integers, ignoring non-numeric fields.

    Args:
        fields (list): A list of strings to process.

    Returns:
        list: A list of integers, with non-numeric fields excluded.
    """
    try:
        return [int(field) for field in fields if field.isdigit()]
    except ValueError as e:
        logging.error(f"Error converting fields to integers: {fields} - {e}")
        return []


def extract_double_semicolon_data(line: str) -> list:
    """
    Extracts data after the last `;;` in a line, often used for lineup extraction.

    Args:
        line (str): The input line to process.

    Returns:
        list: A list of numbers found after the `;;`.
    """
    parts = line.strip().split(";")
    try:
        double_semicolon_index = next(
            i for i in range(len(parts) - 1) if parts[i] == "" and parts[i + 1] == ""
        )
        data = parts[double_semicolon_index + 2 :]
        extracted_data = extract_numeric_fields(data)
        logging.debug(f"Data after `;;`: {extracted_data}")
        return extracted_data
    except StopIteration:
        logging.error(f"Double semicolon (`;;`) not found in line: {line}")
        return []


def find_team_type(line: str) -> str | None:
    """
    Determines the team type (home or away) from the line prefix.

    Args:
        line (str): The input line to inspect.

    Returns:
        str: "home" if the line corresponds to the home team, "away" otherwise.
    """
    if line.startswith("*"):
        return "home"
    if line.startswith("a"):
        return "away"
    logging.warning(f"Unable to determine team type for line: {line}")
    return None


def is_valid_action_line(line: str) -> bool:
    """
    Check if the line is a valid action line.

    Args:
        line (str): The input line to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return (
        len(line) >= 4
        and line[0] in {"*", "a"}
        and line[1:3].isdigit()
        and line[3] in SKILL_DICT
    )


def parse_action_line(line: str) -> dict | None:
    """
    Parse a single action line into a structured dictionary.

    Args:
        line (str): The input line to parse.

    Returns:
        dict | None: Parsed action line data or None if invalid.
    """
    if not is_valid_action_line(line):
        logging.debug(f"Ignored invalid action line: {line}")
        return None

    try:
        team = find_team_type(line)
        player_number = int(line[1:3]) if line[1:3].isdigit() else None
        skill = SKILL_DICT.get(line[3], "unknown")
        skill_type = SKILL_TYPE_DICT.get(line[4], "unknown") if len(line) > 4 else None
        result_action = (
            RESULT_ACTION_DICT.get(line[5], "unknown") if len(line) > 5 else None
        )

        parts = line.split(";")
        local_timestamp = next(
            (part.strip() for part in parts if "." in part and part.count(".") == 2),
            None,
        )
        raw_data = parts[6].strip() if len(parts) > 6 else None

        # Generate action_id from the line
        action_id = f"{team}_{player_number}_{skill}_{skill_type}_{result_action}"

        return {
            "action_id": action_id,
            "line": line.strip(),
            "team": team,
            "player_number": player_number,
            "skill": skill,
            "skill_type": skill_type,
            "result_action": result_action,
            "raw_data": raw_data,
            "local_timestamp": local_timestamp,
            "video_timestamp": "",
        }
    except Exception as e:
        logging.error(f"Error parsing action line: {line} - {e}")
        return None


def is_default_action_line(line: str) -> bool:
    """
    Checks if a line is a special case like *$$&H# or a$$&H#.

    Args:
        line (str): The line to check.

    Returns:
        bool: True if it matches the pattern, False otherwise.
    """
    return re.match(r"^[\*\a]\$\$&H#", line)


def parse_default_action_line(line: str) -> dict:
    """
    Parses special lines like *$$&H# or a$$&H# and returns a placeholder action.

    Args:
        line (str): The input line to parse.

    Returns:
        dict: Placeholder action data.
    """
    local_timestamp_match = re.search(r"\d{2}\.\d{2}\.\d{2}", line)
    local_timestamp = (
        local_timestamp_match.group(0) if local_timestamp_match else "00:00:00"
    )

    return {
        "line": line,
        "team": "unknown",
        "player_number": -1,
        "skill": "unknown",
        "skill_type": "unknown",
        "result_action": "unknown",
        "raw_data": "unknown",
        "local_timestamp": local_timestamp,
        "video_timestamp": "",
    }


def extract_timestamp(parts: list[str]) -> str | None:
    """
    Extract the timestamp from line parts.
    """
    return next(
        (part.strip() for part in parts if "." in part and part.count(".") == 2), None
    )
