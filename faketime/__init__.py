from datetime import datetime as dt


class FakeTime:

    def __init__(self):
        self.offset = 0

    @staticmethod
    def get_now():
        return dt.now()
