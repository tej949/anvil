class TopologyMapper:

    def __init__(self):

        self.alias_map = {}

    def process_event(self, event):

        if (
            event.get("kind") == "topology"
            and event.get("change") == "rename"
        ):

            old = event["from_"]
            new = event["to"]

            canonical = self.alias_map.get(
                old,
                old
            )

            self.alias_map[new] = canonical

    def resolve(self, service):

        return self.alias_map.get(
            service,
            service
        )