"""Functions that interact with the Postcode API."""

import requests
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...


def validate_postcode(postcode: str) -> bool:
    """Checks if given postcode is valid"""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    api = f"https://api.postcodes.io/postcodes/{postcode}/validate"
    response = requests.get(api, timeout=5)
    if response.status_code == 200:
        return response.json()["result"]
    elif response.status_code == 500:
        raise requests.RequestException("Unable to access API.")
    raise Exception("Could not fetch from the API")


def get_postcode_for_location(lat: float, long: float) -> str:
    """Retrieves postcode associated with given longitude and latitude"""
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    api = f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"
    response = requests.get(api, timeout=5)
    if response.status_code == 200:
        if response.json()["result"] == None:
            raise ValueError("No relevant postcode found.")
        results = response.json()["result"]
        best_result = results[0]
        return best_result["postcode"]
    elif response.status_code == 500:
        raise requests.RequestException("Unable to access API.")
    raise Exception("Could not fetch from the API")


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Returns completed postcodes from the beginning of a postcode"""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    api = f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"
    response = requests.get(api, timeout=5)
    if response.status_code == 500:
        raise requests.RequestException("Unable to access API.")
    results = response.json()["result"]
    return results


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Returns details on up to 100 postcodes"""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")

    for item in postcodes:
        if not isinstance(item, str):
            raise TypeError("Function expects a list of strings.")

    api = f"https://api.postcodes.io/postcodes"
    response = requests.post(api, json={"postcodes": postcodes}, timeout=5)

    if response.status_code == 500:
        raise requests.RequestException("Unable to access API.")

    return response.json()["result"]
