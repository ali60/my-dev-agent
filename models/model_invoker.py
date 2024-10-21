from abc import ABC, abstractmethod



class ModelInvoker(ABC):
    def __init__(self, model_id):
        self.model_id = model_id

    @abstractmethod
    def invoke(self, prompt, payload=None):
        """This method should be implemented by subclasses to invoke the specific model."""
        pass

    @abstractmethod
    def process_response(self, response):
        """Process the response returned by the model."""
        pass
