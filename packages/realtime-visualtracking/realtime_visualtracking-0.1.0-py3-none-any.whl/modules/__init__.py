import requests

class VisualTracking:
    def __init__(self, token):
        self.token = token

    def track(self, transactionId, phaseName):
        try:
            url = "https://api.infsite.org/br-websocket/track"

            payload = {
                        "transactionId": transactionId,
                        "tracking": [
                            {
                                "phaseName": phaseName
                            }
                        ]
                    }
            headers = {
            "token": self.token
            }

            response = requests.request("POST", url, headers=headers, json=payload)
        except Exception as error:
            pass
