from datetime import datetime


class FingerprintBuilder:

    IMPORTANT_KINDS = {
        "deploy",
        "metric",
        "log",
        "incident_signal",
        "remediation",
    }

    def parse_ts(self, ts):

        try:

            return datetime.fromisoformat(
                ts.replace("Z", "+00:00")
            )

        except Exception:

            return None

    def build(self, events):

        sequence = []

        services = set()

        # temporal tracking
        deploy_ts = None
        timeout_ts = None

        latency_events = []

        ordered_events = sorted(
            events,
            key=lambda e: e.get("ts", "")
        )

        for event in ordered_events:

            kind = event.get("kind")

            if kind not in self.IMPORTANT_KINDS:
                continue

            canonical_service = event.get(
                "canonical_service",
                event.get("service", "unknown")
            )

            services.add(canonical_service)

            token = kind

            # metric events
            if kind == "metric":

                metric_name = event.get(
                    "name",
                    "metric"
                ).lower()

                value = event.get(
                    "value",
                    0
                )

                # latency metrics
                if "latency" in metric_name:

                    latency_events.append(value)

                    if value > 1000:
                        severity = "critical"

                    elif value > 300:
                        severity = "high"

                    else:
                        severity = "normal"

                    token += (
                        f":latency:{severity}"
                    )

                # error metrics
                elif "error" in metric_name:

                    if value > 0.5:
                        severity = "critical"

                    elif value > 0.2:
                        severity = "high"

                    else:
                        severity = "normal"

                    token += (
                        f":error_rate:{severity}"
                    )

                else:

                    token += f":{metric_name}"

            # log events
            elif kind == "log":

                msg = event.get(
                    "msg",
                    ""
                ).lower()

                if "timeout" in msg:

                    token += ":timeout"

                    timeout_ts = self.parse_ts(
                        event.get("ts")
                    )

                elif "exception" in msg:

                    token += ":exception"

                else:

                    level = event.get(
                        "level",
                        "info"
                    )

                    token += f":{level}"

            # deploy events
            elif kind == "deploy":

                token += ":deploy"

                deploy_ts = self.parse_ts(
                    event.get("ts")
                )

            # remediation events
            elif kind == "remediation":

                action = event.get(
                    "action",
                    "unknown"
                )

                token += f":{action}"

            sequence.append(token)

        # -----------------------------------
        # TEMPORAL FAILURE DENSITY SIGNALS
        # -----------------------------------

        # rapid deployment failure
        if deploy_ts and timeout_ts:

            delta = (
                timeout_ts - deploy_ts
            ).total_seconds()

            if delta < 120:

                sequence.append(
                    "pattern:rapid_failure"
                )

            elif delta > 1800:

                sequence.append(
                    "pattern:slow_failure"
                )

        # latency degradation pattern
        if len(latency_events) >= 2:

            increasing = all(
                latency_events[i]
                <= latency_events[i + 1]
                for i in range(
                    len(latency_events) - 1
                )
            )

            if increasing:

                sequence.append(
                    "pattern:slow_degradation"
                )

        return {
            "sequence": sequence,
            "services": list(services),
        }