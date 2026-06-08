
import uuid

def to_dict(row) -> dict:
    
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
    
    return [to_dict(r) for r in rows]
