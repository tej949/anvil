"""
Anvil Engine implementation - Persistent Context Engine for P-02.
"""

from pathlib import Path
import sys

# Path to benchmark folder
BENCH_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "bench-p02-context"
)

# Add benchmark folder to Python path
sys.path.insert(0, str(BENCH_ROOT))

try:
    from adapter import Adapter

except ImportError as e:

    raise ImportError(
        f"Failed to import Adapter from benchmark folder. "
        f"Expected at: {BENCH_ROOT / 'adapter.py'}. "
        f"Error: {e}"
    ) from e

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

        # graph memory
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

        # local event cache
        self.events = []

    def ingest(self, events):

        events = list(events)

        # ingest events
        self.ingestor.ingest(events)

        # build temporal graph edges
        build_temporal_edges(
            self.graph,
            events
        )

        # store locally
        self.events.extend(events)

        # learn historical incident patterns
        for event in events:

            if (
                event.get("kind")
                == "incident_signal"
            ):

                incident_id = event.get(
                    "incident_id",
                    f"incident-{len(self.events)}"
                )

                service = event.get(
                    "service",
                    "unknown"
                )

                # nearby events
                related_events = (
                    self.ingestor.get_events_near_signal(
                        event,
                        window_seconds=900
                    )
                )

                # default remediation
                remediation = "rollback"

                # find nearby remediation
                for nearby in related_events:

                    if (
                        nearby.get("kind")
                        == "remediation"
                    ):

                        remediation = nearby.get(
                            "action",
                            "rollback"
                        )

                        break

                # learn incident fingerprint
                self.reconstructor.learn_from_history(
                    incident_id=incident_id,
                    events=related_events,
                    remediation=remediation,
                    service=service,
                )

    def reconstruct_context(
        self,
        signal,
        mode="fast"
    ):

        related_events = (
            self.ingestor.get_events_near_signal(
                signal
            )
        )

        return self.reconstructor.reconstruct(
            signal,
            related_events
        )

    def close(self):

        pass