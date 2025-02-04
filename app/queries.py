"""Database queries for bird name lookups.

This module handles SQLite database operations for mapping between scientific
and common bird names.
"""

import sqlite3


def get_common_name(scientific_name: str) -> str:
    """Get common name for a bird from its scientific name.

    Args:
        scientific_name: Scientific (Latin) name of the bird species

    Returns:
        Common name of the bird species, or "Unknown Bird" if not found
    """
    try:
        conn = sqlite3.connect("data/birdnames.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT common_name FROM birdnames WHERE scientific_name = ?",
            (scientific_name,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            print(f"No common name found for: {scientific_name}")
            return "Unknown Bird"
    except Exception as e:
        print(f"Error looking up bird name: {str(e)}")
        return "Unknown Bird"
