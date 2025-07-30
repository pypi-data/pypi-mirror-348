"""
File containing functions for handling JSON Clippings file.
"""

import json
import os
from typing import Any


def generate_json(clippings: list[dict[str, Any]], output_path: str):
    """
    In provided output_path creates JSON file containing data collected from Clippings input file.

    Args:
        clippings (list[dict]): List of collected Clippings.
        output_path (str): Full path to output file.

    Returns:
        dict: Dictionary containing data about potential errors.
    """

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(clippings, json_file, ensure_ascii=False, indent=4)
    except PermissionError as e:
        return {"error": e}
    return {}
