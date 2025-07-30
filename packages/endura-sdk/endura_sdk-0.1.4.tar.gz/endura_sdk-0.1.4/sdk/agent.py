from .core import get_status, post_status

class DeviceAgent:
    def __init__(self, model):
        self.model = model

    def get_status(self):
        return get_status(self.model)

    def post_status(self):
        return post_status(self.model)