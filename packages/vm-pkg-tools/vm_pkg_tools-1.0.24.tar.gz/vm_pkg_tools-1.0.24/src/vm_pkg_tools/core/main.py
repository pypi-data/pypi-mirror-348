import os
import json
import logging
import argparse
import uuid
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from vm_pkg_tools.core.orchestrator import parse_dvw_file
from vm_pkg_tools.utils.file_utils import read_scout_file
from vm_pkg_tools.utils.logger import setup_logging

# Configure logging with appropriate levels for console and file
setup_logging(console_level=logging.INFO, file_level=logging.DEBUG)


def ensure_directory_exists(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


def main(input_file=None, output_file=None):
    """
    Main entry point for parsing scout files.
    """
    input_file = input_file or os.path.join("data", "scouts", "&1004.dvw")

    # Genenate a dynamic match ID for output file
    match_id = str(uuid.uuid4())[:8]
    output_file = output_file or os.path.join("output", "json", f"{match_id}.json")

    try:
        logging.info(f"Starting scout file parsing: {input_file}")

        scout_content = read_scout_file(input_file)
        if not scout_content:
            logging.error(f"Failed to read scout file: {input_file}")
            return

        parsed_data = parse_dvw_file(scout_content)
        if not parsed_data or all(not v for v in parsed_data.values()):
            logging.error("Parsed data is empty. Check the parser logic.")
            return

        ensure_directory_exists(output_file)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)

        logging.info(f"Successfully wrote the output to: {output_file}")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a DVW scout file.")
    parser.add_argument(
        "--input_file",
        type=str,
        help="Path to the input scout file.",
        required=False,
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="Path to save the parsed output.",
        required=False,
    )
    args = parser.parse_args()
    main(input_file=args.input_file, output_file=args.output_file)
