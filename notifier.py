import requests
import os
import logging


class Notifier:
    def __init__(self, source_1, source_2):
        self.topic = os.getenv('WINDOW_OPEN_NTFY_TOPIC')
        self.target_url = "https://ntfy.sh/" + self.topic
        self.open_request_headers = {"title": "Open windows?"}
        self.source_1 = source_1
        self.source_2 = source_2
        self.logger = logging.getLogger(__name__)

    def send_open_request(self):
        response = requests.post(self.target_url, str(self.source_1) + "\n" + str(self.source_2), self.open_request_headers)
        if response.status_code != 200:
            self.logger.error("Error sending open request")
            self.logger.error(response.status_code)
        return response
