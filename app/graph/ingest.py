from app.graph.topology import (
    TopologyMapper
)

from app.utils.time import (
    time_difference_seconds
)


class GraphIngestor:

    def __init__(self, graph):

        self.graph = graph

        self.topology = TopologyMapper()

        self.events = []

    def ingest(self, events):

        for event in events:

            # process topology updates
            self.topology.process_event(event)

            # resolve canonical service name
            if "service" in event:

                event["canonical_service"] = (
                    self.topology.resolve(
                        event["service"]
                    )
                )

            # add to graph
            self.graph.add_event(event)

            # local event storage
            self.events.append(event)

    def get_events_near_signal(
        self,
        signal,
        window_seconds=3600
    ):

        signal_ts = signal["ts"]

        related = []

        for event in self.events:

            diff = time_difference_seconds(
                signal_ts,
                event["ts"]
            )

            if diff <= window_seconds:

                related.append(event)

        return related