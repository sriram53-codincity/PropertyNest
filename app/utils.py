"""
utils.py  —  One helper to convert psycopg2 rows to plain dicts
"""
import uuid


def to_dict(row) -> dict:
    """Turn a psycopg2 row into a regular dict (converts UUIDs and dates to strings)."""
    if row is None:
        return None
    result = {}
    for key, val in dict(row).items():
        if isinstance(val, uuid.UUID):
            result[key] = str(val)
        elif hasattr(val, "isoformat"):   # date / datetime
            result[key] = val.isoformat()
        else:
            result[key] = val
    return result


def to_list(rows) -> list:
    """Turn a list of psycopg2 rows into a list of dicts."""
    return [to_dict(r) for r in rows]
