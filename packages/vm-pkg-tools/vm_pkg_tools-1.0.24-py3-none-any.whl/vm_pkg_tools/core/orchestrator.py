import logging
import sys
from vm_pkg_tools.parsers.metadata.metadata_parser import parse_metadata
from vm_pkg_tools.parsers.metadata.comments_parser import parse_comments
from vm_pkg_tools.parsers.teams_and_players.teams_parser import parse_teams
from vm_pkg_tools.parsers.teams_and_players.players_parser import parse_players
from vm_pkg_tools.parsers.match_actions.lineups_parser import parse_lineups
from vm_pkg_tools.parsers.sets_results.sets_parser import parse_sets
from vm_pkg_tools.parsers.match_actions.match_actions_parser import parse_match_actions
from vm_pkg_tools.parsers.advanced.parse_more import parse_more


# Define constants for static placeholders, which need to be replaced with actual data.
VIDEO_PLACEHOLDER = "[3VIDEO]"
SETTER_CALL_PLACEHOLDER = "[3SETTERCALL]"
ATTACK_COMBINATIONS_PLACEHOLDER = "[3ATTACKCOMBINATION]"


def parse_dvw_file(content):
    """
    Parses the scout file and returns a structured output.
    """
    try:
        logging.info("Starting metadata and match info parsing.")
        metadata = parse_metadata(content)
        match_info = parse_teams(content)
        match_info.update(parse_more(content))

        logging.info("Parsing sets, lineups, and points.")
        sets = parse_sets(content)
        logging.debug(f"Content snippet for lineups: {content[:500]}")
        lineups = parse_lineups(content)
        logging.debug(f"Content snippet for match actions: {content[:500]}")
        logging.debug(f"Lineups passed to parse_match_actions: {lineups}")
        match_actions = parse_match_actions(content, lineups)
        logging.info(f"match_actions type: {type(match_actions)}")

        logging.info("Parsing players and comments.")
        players_home = parse_players(content, "home")
        players_away = parse_players(content, "away")
        comments = parse_comments(content)

        logging.info("Combining parsed data.")
        return {
            "metadata": metadata,
            "match_info": match_info,
            "comments": comments,
            "players": {"home": players_home, "away": players_away},
            "sets_summary": sets,
            # "starting_lineups": lineups,
            "match_actions": match_actions,
            "media_info": VIDEO_PLACEHOLDER,
            "setter_call": SETTER_CALL_PLACEHOLDER,
            "attack_combinations": ATTACK_COMBINATIONS_PLACEHOLDER,
        }

    except Exception as e:
        logging.error(
            f"Error parsing scout file: {e} - [{__file__}:{sys._getframe().f_lineno}]"
        )
        raise
