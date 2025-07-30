from .core import get_status, post_status

class DeviceAgent:
    def __init__(self, model):
        self.model = model
        self.status = {"health": "initializing"}

    def update_status(self, new_status):
        self.status.update(new_status)

    def get_status(self):
        return get_status(self.model)

    def post_status(self):
        return post_status(self.model)

    def log_inference(self, input_data):
        try:
            output = self.model(input_data)
            self.update_status({"last_output": output.tolist()})
            return output
        except Exception as e:
            self.update_status({"last_error": str(e)})
            raise