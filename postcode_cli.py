"""A CLI application for interacting with the Postcode API."""

import argparse
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode")
    parser.add_argument("postcodead")
    args = parser.parse_args()
