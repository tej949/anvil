class IncidentMemory:

    def __init__(self):

        self.incidents = []

    def add_incident(
        self,
        incident_id,
        fingerprint,
        remediation,
        service,
    ):

        self.incidents.append({
            "incident_id": incident_id,
            "fingerprint": fingerprint,
            "remediation": remediation,
            "service": service,
        })

    def get_all(self):

        return self.incidents