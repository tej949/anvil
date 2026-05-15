class ContextReconstructor:

    def reconstruct(
        self,
        signal,
        related_events
    ):

        return {
            "related_events": related_events,
            "causal_chain": [],
            "similar_past_incidents": [],
            "suggested_remediations": [],
            "confidence": 0.5,
            "explain": (
                "Initial reconstruction"
            )
        }