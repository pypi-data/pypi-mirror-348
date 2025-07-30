import logging
from unidecode import unidecode
from vm_pkg_tools.utils.parser_utils import extract_section
from vm_pkg_tools.validators.data_validator import validate_data


def transliterate(value):
    """
    Transliterates a given string to ASCII-compatible characters.

    Args:
        value (str): The string to transliterate.

    Returns:
        str: Transliterated string.
    """
    return unidecode(value)


def parse_metadata(content):
    """
    Parses the [3DATAVOLLEYSCOUT] section from the scout file content.

    Args:
        content (str): The full scout file content.

    Returns:
        dict: A dictionary containing metadata details.
    """
    try:
        # Extract metadata section
        section = extract_section(content, "3DATAVOLLEYSCOUT")
        if not section:
            logging.warning("[3DATAVOLLEYSCOUT] section not found.")
            return {"generator": {}, "last_change": {}, "file_format": None}

        lines = section.splitlines()
        metadata = {"generator": {}, "last_change": {}}

        # Process each line to extract metadata details
        for line in lines:
            if line.startswith("FILEFORMAT:"):
                metadata["file_format"] = transliterate(line.split(":")[1].strip())
            elif line.startswith("GENERATOR-"):
                key = line.split("-")[1].split(":")[0].lower()
                value = transliterate(line.split(":")[1].strip())
                metadata["generator"][key] = value
            elif line.startswith("LASTCHANGE-"):
                key = line.split("-")[1].split(":")[0].lower()
                value = transliterate(line.split(":")[1].strip())
                metadata["last_change"][key] = value

        # Validate the parsed metadata
        is_valid, validation_message = validate_data(metadata)
        if not is_valid:
            logging.error(f"Validation failed for metadata: {validation_message}")
            return {"generator": {}, "last_change": {}, "file_format": None}

        logging.info(f"Parsed metadata: {metadata}")
        return metadata
    except Exception as e:
        logging.error(f"Error parsing metadata: {e}")
        return {"generator": {}, "last_change": {}, "file_format": None}
