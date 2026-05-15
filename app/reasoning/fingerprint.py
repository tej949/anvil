class FingerprintBuilder:

    IMPORTANT_KINDS = {
        "deploy",
        "metric",
        "log",
        "incident_signal",
        "remediation",
    }

    def build(self, events):

        sequence = []

        services = set()

        for event in events:

            kind = event.get("kind")

            if kind not in self.IMPORTANT_KINDS:
                continue

            canonical_service = event.get(
                "canonical_service",
                event.get("service", "unknown")
            )

            services.add(canonical_service)

            token = kind

            # ---- metric events ----
            if kind == "metric":

                metric_name = event.get(
                    "name",
                    "metric"
                )

                token += f":{metric_name}"

            # ---- log events ----
            elif kind == "log":

                msg = event.get(
                    "msg",
                    ""
                ).lower()

                if "timeout" in msg:

                    token += ":timeout"

                else:

                    level = event.get(
                        "level",
                        "info"
                    )

                    token += f":{level}"

            # ---- deploy events ----
            elif kind == "deploy":

                token += ":deploy"

            # ---- remediation ----
            elif kind == "remediation":

                action = event.get(
                    "action",
                    "unknown"
                )

                token += f":{action}"

            sequence.append(token)

        return {
            "sequence": sequence,
            "services": list(services),
        }