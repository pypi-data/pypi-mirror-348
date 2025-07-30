import logging
from jsonschema import validate, ValidationError


def validate_schema(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        logging.error(f"Schema validation error: {e}")
        return False, str(e)
