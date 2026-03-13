"""Functions that interact with the Postcode API."""

import os
import json
import requests

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="UTF-8") as f:
            cache = json.load(f)
        return cache
    return {}


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, "w", encoding="UTF-8") as f:
        json.dump(cache, f)


def validate_postcode(postcode: str) -> bool:
    """Checks if given postcode is valid"""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    cache = load_cache()

    if postcode in cache and "valid" in cache[postcode]:
        return cache[postcode]["valid"]

    api = f"https://api.postcodes.io/postcodes/{postcode}/validate"
    response = requests.get(api, timeout=5)

    if response.status_code == 200:
        result = response.json()["result"]

        if postcode not in cache:
            cache[postcode] = {}

        cache[postcode]["valid"] = result
        save_cache(cache)

        return result

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
        if response.json()["result"] is None:
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

    cache = load_cache()

    if postcode_start in cache and "completions" in cache[postcode_start]:
        return cache[postcode_start]["completions"]

    api = f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"
    response = requests.get(api, timeout=5)
    if response.status_code == 500:
        raise requests.RequestException("Unable to access API.")
    results = response.json()["result"] or []

    if postcode_start not in cache:
        cache[postcode_start] = {}

    cache[postcode_start]["completions"] = results
    save_cache(cache)

    return results


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Returns details on up to 100 postcodes"""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")

    for item in postcodes:
        if not isinstance(item, str):
            raise TypeError("Function expects a list of strings.")

    api = "https://api.postcodes.io/postcodes"
    response = requests.post(api, json={"postcodes": postcodes}, timeout=5)

    if response.status_code == 500:
        raise requests.RequestException("Unable to access API.")

    return response.json()["result"]
