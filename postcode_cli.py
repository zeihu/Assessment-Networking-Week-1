"""A CLI application for interacting with the Postcode API."""

import argparse

from postcode_functions import validate_postcode, get_postcode_completions


def mode_selection(mode: str, postcode) -> str:
    """Returns string based on given mode and postcode"""
    if mode == "validate":
        if validate_postcode(postcode) is True:
            return f"{postcode} is a valid postcode."
        return f"{postcode} is not a valid postcode."

    if mode == "complete":
        completions = get_postcode_completions(postcode) or []

        if len(completions) == 0:
            return f"No matches for {postcode}."

        return "\n".join(completions[:5])

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m", required=True,
                        choices=["validate", "complete"])
    parser.add_argument("postcode")
    args = parser.parse_args()

    postcode = args.postcode.lstrip().rstrip().upper()
    mode = args.mode

    print(mode_selection(mode, postcode))
