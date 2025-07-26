import requests
import os


class Notifier:
    def __init__(self, source_1, source_2):
        self.topic = os.getenv('WINDOW_OPEN_NTFY_TOPIC')
        self.target_url = "https://ntfy.sh/" + self.topic
        self.open_request_headers = {"title": "Open windows?"}
        self.source_1 = source_1
        self.source_2 = source_2

    def send_open_request(self):
        return requests.post(self.target_url, str(self.source_1) + "\n" + str(self.source_2), self.open_request_headers)
