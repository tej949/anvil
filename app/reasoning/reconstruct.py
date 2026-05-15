from .fingerprint import (
    FingerprintBuilder
)

from .similarity import (
    SimilarityEngine
)

from .memory import (
    IncidentMemory
)

from ..utils.time import (
    parse_timestamp
)


class ContextReconstructor:

    def __init__(
        self,
        graph=None
    ):

        self.graph = graph

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

        # sort related events temporally
        related_events = sorted(
            related_events,
            key=lambda e: parse_timestamp(
                e.get("ts", "")
            )
        )

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

            # precision filtering
            if similarity >= 0.40:

                matches.append({
                    "incident_id": historical["incident_id"],
                    "similarity": similarity,
                    "rationale": (
                        "behavioral pattern match"
                    ),
                    "remediation": historical["remediation"],
                })

        # sort descending
        matches.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        # remove duplicates
        seen = set()

        unique_matches = []

        for match in matches:

            incident_id = match["incident_id"]

            if incident_id in seen:
                continue

            seen.add(incident_id)

            unique_matches.append(match)

        # top 5
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

        # build causal chain
        causal_chain = []

        event_sequence = []

        has_deploy = False
        has_timeout = False
        has_latency = False

        previous_event = None

        for event in related_events:

            kind = event.get("kind")

            if not kind:
                continue

            service = event.get(
                "canonical_service",
                event.get("service")
            )

            ts = event.get("ts")

            event_id = (
                event.get("event_id")
                or f"{kind}:{service}:{ts}"
            )

            event_entry = {
                "event_type": kind,
                "service": service,
                "timestamp": ts,
                "event_id": event_id,
            }

            # enrich metrics
            if kind == "metric":

                metric_name = event.get(
                    "name",
                    "unknown_metric"
                )

                event_entry["metric"] = metric_name

                if "latency" in metric_name:
                    has_latency = True

                event_sequence.append(
                    f"metric({metric_name})"
                )

            # enrich logs
            elif kind == "log":

                msg = event.get(
                    "msg",
                    ""
                ).lower()

                if "timeout" in msg:

                    has_timeout = True

                    event_entry["signal"] = (
                        "timeout"
                    )

                    event_sequence.append(
                        "log(timeout)"
                    )

                else:

                    level = event.get(
                        "level",
                        "info"
                    )

                    event_entry["level"] = level

                    event_sequence.append(
                        f"log({level})"
                    )

            # deploy tracking
            elif kind == "deploy":

                has_deploy = True

                event_sequence.append(
                    f"deploy({service})"
                )

            # remediation tracking
            elif kind == "remediation":

                action = event.get(
                    "action",
                    "unknown"
                )

                event_entry["action"] = action

                event_sequence.append(
                    f"remediation({action})"
                )

            else:

                event_sequence.append(kind)

            # causal edge generation
            if previous_event:

                previous_kind = previous_event.get(
                    "kind"
                )

                previous_service = previous_event.get(
                    "canonical_service",
                    previous_event.get("service")
                )

                previous_ts = previous_event.get(
                    "ts"
                )

                previous_event_id = (
                    previous_event.get("event_id")
                    or (
                        f"{previous_kind}:"
                        f"{previous_service}:"
                        f"{previous_ts}"
                    )
                )

                causal_chain.append({
                    "cause_event_id":
                        previous_event_id,

                    "effect_event_id":
                        event_id,

                    "evidence": (
                        "temporal event progression"
                    ),

                    "confidence": 0.7,
                })

            previous_event = event

        # root cause hints
        likely_root_cause = (
            "unknown operational anomaly"
        )

        if has_deploy and has_timeout:

            likely_root_cause = (
                "possible deployment regression"
            )

        elif has_latency and has_timeout:

            likely_root_cause = (
                "possible downstream service saturation"
            )

        elif has_latency:

            likely_root_cause = (
                "possible performance degradation"
            )

        # confidence
        confidence = (
            top_matches[0]["similarity"]
            if top_matches
            else 0.3
        )

        # dynamic explanation
        explanation = (
            "Detected operational similarity using "
            "behavioral fingerprints, temporal event "
            "ordering, topology-aware service identity "
            "resolution, and remediation memory. "
        )

        if event_sequence:

            explanation += (
                "Observed sequence: "
                + " → ".join(event_sequence[:6])
            )

        explanation += (
            f" Likely root cause: "
            f"{likely_root_cause}."
        )

        return {

            "related_events": related_events,

            "causal_chain": causal_chain,

            "likely_root_cause":
                likely_root_cause,

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

            "explain": explanation,
        }

