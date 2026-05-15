import networkx as nx


class OperationalMemoryGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_event(self, event):

        event_id = self._make_event_id(event)

        self.graph.add_node(
            event_id,
            **event
        )

        return event_id

    def add_edge(
        self,
        source,
        target,
        relation,
        confidence=1.0
    ):

        self.graph.add_edge(
            source,
            target,
            relation=relation,
            confidence=confidence
        )

    def get_neighbors(self, event_id):

        return list(
            self.graph.neighbors(event_id)
        )

    def get_node(self, event_id):

        return self.graph.nodes[event_id]

    def _make_event_id(self, event):

        ts = event.get("ts", "")
        kind = event.get("kind", "")
        svc = event.get("service", "")

        return f"{kind}:{svc}:{ts}"