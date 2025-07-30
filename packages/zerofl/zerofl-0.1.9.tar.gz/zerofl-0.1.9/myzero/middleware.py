class MiddlewareManager:
    def __init__(self):
        self.before_request = []

    def add(self, func):
        self.before_request.append(func)
