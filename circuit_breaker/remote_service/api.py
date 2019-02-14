from time import sleep


class API:
    def __init__(self):
        self.data = []

    def handle_post(self, wait, status_code):
        sleep(wait)
        data = {
            'wait': wait,
            'status_code': status_code,
        }
        return data
