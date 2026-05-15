class FingerprintBuilder:

    def build(self, events):

        return {
            "sequence": [
                e.get("kind")
                for e in events
            ],

            "services": list(set(
                e.get(
                    "canonical_service",
                    e.get("service")
                )
                for e in events
            )),
        }