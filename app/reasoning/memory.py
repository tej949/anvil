class IncidentMemory:

    def __init__(self):

        self.memory = []

    def store(
        self,
        incident_id,
        fingerprint,
        remediation
    ):

        self.memory.append({
            "incident_id": incident_id,
            "fingerprint": fingerprint,
            "remediation": remediation
        })

    def all(self):

        return self.memory