from datetime import datetime


def parse_ts(ts):

    return datetime.fromisoformat(
        ts.replace("Z", "+00:00")
    )


def build_temporal_edges(
    graph,
    events
):

    events = sorted(
        events,
        key=lambda e: e["ts"]
    )

    for i in range(len(events) - 1):

        a = events[i]
        b = events[i + 1]

        a_id = graph._make_event_id(a)
        b_id = graph._make_event_id(b)

        graph.add_edge(
            a_id,
            b_id,
            relation="temporal"
        )