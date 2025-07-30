import logging
from vm_pkg_tools.utils.parser_utils import extract_section
from vm_pkg_tools.validators.data_validator import validate_data


def parse_comments(content):
    """
    Parses the [3COMMENTS] section from the scout file content.

    Args:
        content (str): The full scout file content.

    Returns:
        dict: A dictionary containing parsed comments or None if not found.
    """
    try:
        comments_section = extract_section(content, "3COMMENTS")
        if not comments_section:
            logging.warning("[3COMMENTS] section not found.")
            return {"comments": None}

        # Clean and validate the comments
        raw_comments = comments_section.strip()
        comments = raw_comments if raw_comments else "No comments"

        parsed_data = {"comments": comments}
        is_valid, validation_message = validate_data(parsed_data)
        if not is_valid:
            logging.error(f"Validation failed for comments: {validation_message}")
            return {"comments": None}

        logging.info(f"Parsed comments: {comments}")
        return parsed_data
    except Exception as e:
        logging.error(f"Error parsing comments: {e}")
        return {"comments": None}
