import logging


def validate_data(data):
    """
    General data validation logic.
    """
    if not data:
        logging.error("Data validation error: Data is empty")
        return False, "Data is empty"

    if not isinstance(data, dict):
        logging.error("Data validation error: Data is not a dictionary")
        return False, "Data is not a dictionary"

    # Add more validation checks as needed
    return True, "Data is valid"
