class TextProcessor:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def summarize_text(self, input_text):
        prompt = f"Summarize the following text: \n{input_text}"
        return self.model_manager.invoke_model(prompt)

    def generate_response(self, input_text):
        prompt = f"Generate a critical response for this text: \n{input_text}"
        return self.model_manager.invoke_model(prompt)

    def reword_response(self, input_text):
        prompt = f"Reword this text: \n{input_text}"
        return self.model_manager.invoke_model(prompt)

    def rewrite_code(self, input_text):
        prompt = f"Enhance this code: \n{input_text}"
        return self.model_manager.invoke_model(prompt)

    def unit_test_code(self, input_text):
        prompt = f"Write unit test for this code, use unittest, use given/then/when: \n{input_text}"
        return self.model_manager.invoke_model(prompt)
