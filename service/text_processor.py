# service/text_processor.py
class TextProcessor:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def summarize_text(self, text):
        prompt = (
            "Please summarize the following text and format your response in markdown:\n\n"
            f"{text}\n\n"
            "Use markdown formatting including:\n"
            "- Headers for main points\n"
            "- Bullet points for key details\n"
            "- Bold/italic for emphasis where appropriate"
        )
        return self.model_manager.invoke_model(prompt)

    def critical_response(self, text):
        prompt = (
            "Please provide a critical analysis of the following text using markdown formatting:\n\n"
            f"{text}\n\n"
            "Include:\n"
            "- Main arguments\n"
            "- Supporting evidence\n"
            "- Potential counterarguments\n"
            "- Your evaluation"
        )
        return self.model_manager.invoke_model(prompt)

    def generate_response(self, text):
        prompt = (
            "Please generate a detailed response to the following text using markdown formatting:\n\n"
            f"{text}"
        )
        return self.model_manager.invoke_model(prompt)

    def rewrite_code(self, text):
        prompt = (
            "Please rewrite and improve the following code. Format your response in markdown:\n\n"
            f"```\n{text}\n```\n\n"
            "Include:\n"
            "- Improved code in a code block\n"
            "- Explanation of changes\n"
            "- Best practices applied"
        )
        return self.model_manager.invoke_model(prompt)

    def generate_unit_test(self, text):
        prompt = (
            "Please generate unit tests for the following code using markdown formatting:\n\n"
            f"```\n{text}\n```\n\n"
            "Include:\n"
            "- Test cases in code blocks\n"
            "- Test coverage explanation\n"
            "- Testing best practices"
        )
        return self.model_manager.invoke_model(prompt)

    def list_typos(self, text):
        prompt = (
            "Please list any typos or grammatical errors in the following text using markdown formatting:\n\n"
            f"{text}\n\n"
            "Format as:\n"
            "- Original text (with error highlighted)\n"
            "- Correction\n"
            "- Explanation"
        )
        return self.model_manager.invoke_model(prompt)

    def code_review(self, text):
        prompt = (
            "Please provide a code review for the following code using markdown formatting:\n\n"
            f"```\n{text}\n```\n\n"
            "Include:\n"
            "- Code quality analysis\n"
            "- Potential improvements\n"
            "- Security considerations\n"
            "- Performance suggestions"
        )
        return self.model_manager.invoke_model(prompt)


    def sec_review(self, text):
        prompt = (
            "Performs a security review analysis on this document using markdown formatting:\n\n"
            "At the end give me the table for the list of concerns with impact etc\n"
            f"```\n{text}\n```\n\n"
        )
        return self.model_manager.invoke_model(prompt)

    def null(self, text):
        return self.model_manager.invoke_model(text)
