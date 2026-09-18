import json


def parse_json_input(value, default=None):
    if not value or not value.strip():
        return default if default is not None else []

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        raise ValueError("Invalid selection.")