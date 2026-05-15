"""
Anvil Engine implementation - Persistent Context Engine for P-02.

This module contains the main Engine class that implements the benchmark's
Adapter interface. It uses the anvil application's graph and reasoning modules
to provide incident context reconstruction.

The Engine is discovered by the benchmark via the bridge module in:
    bench-p02-context/adapters/mine.py
"""
from pathlib import Path
import sys

# Get path to benchmark directory for importing the base Adapter class
BENCH_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "bench-p02-context"
)

# Add bench-p02-context to path to import base adapter and schema
sys.path.insert(0, str(BENCH_ROOT))

try:
    from adapter import Adapter
except ImportError as e:
    raise ImportError(
        f"Failed to import Adapter from benchmark folder. "
        f"Expected at: {BENCH_ROOT / 'adapter.py'}. "
        f"Error: {e}"
    ) from e

# Import from anvil application modules
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