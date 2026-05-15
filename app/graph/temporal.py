from ..utils.time import (
    parse_timestamp
)


def build_temporal_edges(
    graph,
    events
):

    ordered_events = sorted(
        events,
        key=lambda e: parse_timestamp(
            e["ts"]
        )
    )

    for i in range(
        len(ordered_events) - 1
    ):

        current_event = ordered_events[i]

        next_event = ordered_events[i + 1]

        current_id = (
            current_event.get("event_id")
            or current_event.get("incident_id")
            or f"{i}"
        )

        next_id = (
            next_event.get("event_id")
            or next_event.get("incident_id")
            or f"{i+1}"
        )

        graph.add_edge(
            current_id,
            next_id,
            "temporal"
        )