import sys
from pathlib import Path

BENCH_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "bench-p02-context"
)

sys.path.append(str(BENCH_ROOT))

from adapter import Adapter

from app.graph import (
    OperationalMemoryGraph,
    GraphIngestor,
    build_temporal_edges
)

from app.reasoning import (
    ContextReconstructor
)
class Engine(Adapter):

    def __init__(self):

        # operational graph memory
        self.graph = (
            OperationalMemoryGraph()
        )

        # ingestion pipeline
        self.ingestor = (
            GraphIngestor(self.graph)
        )

        # reasoning engine
        self.reconstructor = (
            ContextReconstructor()
        )

        # local cache of events
        self.events = []

    def ingest(self, events):

        events = list(events)

        # ingest into graph
        self.ingestor.ingest(events)

        # build temporal relationships
        build_temporal_edges(
            self.graph,
            events
        )

        # store locally
        self.events.extend(events)

    def reconstruct_context(
        self,
        signal,
        mode="fast"
    ):

        service = signal.get("service")

        related_events = []

        # simple retrieval
        for event in self.events:

            if (
                event.get("service")
                == service
            ):

                related_events.append(
                    event
                )

        # last 10 relevant events
        related_events = (
            related_events[-10:]
        )

        return self.reconstructor.reconstruct(
            signal,
            related_events
        )

    def close(self):

        # benchmark requires this
        pass