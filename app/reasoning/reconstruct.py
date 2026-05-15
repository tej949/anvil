from app.reasoning.fingerprint import (
    FingerprintBuilder
)

from app.reasoning.similarity import (
    SimilarityEngine
)

from app.reasoning.memory import (
    IncidentMemory
)


class ContextReconstructor:

    def __init__(self):

        self.fingerprint_builder = (
            FingerprintBuilder()
        )

        self.similarity_engine = (
            SimilarityEngine()
        )

        self.memory = (
            IncidentMemory()
        )

    def learn_from_history(
        self,
        incident_id,
        events,
        remediation,
        service,
    ):

        fingerprint = (
            self.fingerprint_builder.build(
                events
            )
        )

        self.memory.add_incident(
            incident_id=incident_id,
            fingerprint=fingerprint,
            remediation=remediation,
            service=service,
        )

    def reconstruct(
        self,
        signal,
        related_events
    ):

        current_fp = (
            self.fingerprint_builder.build(
                related_events
            )
        )

        matches = []

        # compare against historical incidents
        for historical in self.memory.get_all():

            similarity = (
                self.similarity_engine.compare(
                    current_fp,
                    historical["fingerprint"]
                )
            )

            if similarity >= 0.20:
                matches.append({
                    "incident_id": historical["incident_id"],
                    "similarity": similarity,
                    "rationale": (
                        "behavioral pattern match"
                    ),
                    "remediation": historical["remediation"],
            })

        # highest similarity first
        matches.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        # remove duplicate incidents
        seen = set()

        unique_matches = []

        for match in matches:

            incident_id = match["incident_id"]

            if incident_id in seen:
                continue

            seen.add(incident_id)

            unique_matches.append(match)

        # top-5 results
        top_matches = unique_matches[:5]

        # remediation suggestions
        suggested_remediations = []

        if top_matches:

            best_match = top_matches[0]

            suggested_remediations.append({
                "action": best_match["remediation"],
                "target": signal.get("service"),
                "historical_outcome": "resolved",
                "confidence": best_match["similarity"],
            })

        confidence = (
            top_matches[0]["similarity"]
            if top_matches
            else 0.3
        )

        return {

            "related_events": related_events,

            "causal_chain": [],

            "similar_past_incidents": [
                {
                    "incident_id": match["incident_id"],
                    "similarity": match["similarity"],
                    "rationale": match["rationale"],
                }
                for match in top_matches
            ],

            "suggested_remediations":
                suggested_remediations,

            "confidence": confidence,

            "explain": (
                "Matched using behavioral "
                "incident fingerprints with "
                "temporal event similarity."
            ),
        }