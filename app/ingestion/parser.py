import json
from app.models.event import Event


def load_events(path: str):
    with open(path, "r") as f:
        raw_events = json.load(f)

    return [Event(**event) for event in raw_events]