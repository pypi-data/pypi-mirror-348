import logging
from vm_pkg_tools.utils.parser_utils import extract_section, parse_line
from vm_pkg_tools.validators.data_validator import validate_data


def parse_more(content):
    """
    Parse the [3MORE] section of the content to extract additional match details.

    Args:
        content (str): The full scout file content.

    Returns:
        dict: A dictionary containing referees, location, venue, and code.
    """
    try:
        # Extract the [3MORE] section
        more_section = extract_section(content, "3MORE")
        if not more_section:
            logging.warning("[3MORE] section not found.")
            return create_default_more_output()

        # Split section into lines
        lines = more_section.strip().splitlines()
        if not lines:
            logging.warning("[3MORE] section is empty.")
            return create_default_more_output()

        # Parse the first line
        first_line_fields = parse_line(lines[0], delimiter=";")
        if len(first_line_fields) < 6:
            logging.warning("[3MORE] section has missing fields.")
            return create_default_more_output()

        # Construct the parsed data
        parsed_data = {
            "referees": first_line_fields[0].strip(),
            "location": first_line_fields[3].strip()
            if len(first_line_fields) > 3
            else None,
            "venue": first_line_fields[4].strip()
            if len(first_line_fields) > 4
            else None,
            "code": first_line_fields[5].strip()
            if len(first_line_fields) > 5
            else None,
        }

        # Validate the parsed data
        is_valid, validation_message = validate_data(parsed_data)
        if not is_valid:
            logging.error(
                f"Validation failed for [3MORE] section: {validation_message}"
            )
            return create_default_more_output()

        return parsed_data

    except Exception as e:
        logging.error(f"Error parsing [3MORE] section: {e}")
        return create_default_more_output()


def create_default_more_output():
    """
    Create a default output for the [3MORE] section.

    Returns:
        dict: Default dictionary with None values for all keys.
    """
    return {
        "referees": None,
        "location": None,
        "venue": None,
        "code": None,
    }
