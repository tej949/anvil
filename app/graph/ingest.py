from app.graph.topology import (
    TopologyMapper
)


class GraphIngestor:

    def __init__(self, graph):

        self.graph = graph

        self.topology = TopologyMapper()

        self.events = []

    def ingest(self, events):

        for event in events:

            self.topology.process_event(event)

            if "service" in event:

                event["canonical_service"] = (
                    self.topology.resolve(
                        event["service"]
                    )
                )

            self.graph.add_event(event)

            self.events.append(event)