import pybreaker
from requests import HTTPError

from http_client import HttpClient

db_breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=10)


class API:
    def __init__(self):
        uri = 'http://localhost:5001/'

        self.client = HttpClient(uri=uri)

    @db_breaker
    def remote_post(self, wait, status_code):
        path = 'handle_post'
        params = {
            'wait': wait,
            'status_code': status_code,
        }
        try:
            response_text = self.client.post(path=path, params=params)
        except HTTPError as e:
            if e.response.status_code >= 500:
                raise

        return response_text
