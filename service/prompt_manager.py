import subprocess
import pyperclip
import time
from service.text_processor import TextProcessor
from models.model_manager import ModelManager


class PromptManager:
    def __init__(self, config):
        self.config = config
        self.model_manager = ModelManager(config)
        self.text_processor = TextProcessor(model_manager=self.model_manager)
       # Dictionary mapping user input to corresponding methods
        self.command_map = {
            "s": self.text_processor.summarize_text,
            "c": self.text_processor.generate_response,
            "r": self.text_processor.reword_response,
            "rc": self.text_processor.rewrite_code,
            "uc": self.text_processor.unit_test_code,
        }

    def get_selected_text(self):
        # Check the OS from the config
        os_type = self.config["os"]

        if os_type == "linux":
            # Simulate Ctrl+C on Linux using xdotool
            subprocess.run(["xdotool", "key", "ctrl+c"])

        elif os_type == "darwin":  # macOS
            # Use AppleScript to simulate Ctrl+C on macOS
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    'tell application "System Events" to keystroke "c" using {command down}',
                ]
            )

        elif os_type == "windows":
            # On Windows, simulate Ctrl+C using the built-in 'clip' functionality (WSL might need adjustment)
            subprocess.run(["powershell.exe", "Get-Clipboard"], stdout=subprocess.PIPE)

        # Allow time for the clipboard to update
        time.sleep(0.1)

        # Get the clipboard content using pyperclip
        selected_text = pyperclip.paste()

        return selected_text

    def run(self):
        print("Press 's' to capture and summarize the selected text, or 'q' to quit.")
        while True:
            user_input = input(
                "[s:summarize, c: critical response, r: response, rc:rewrite_code, uc:generate unit test]  "
            ).lower()
            text = self.get_selected_text()
            
            if not text:
                print("No text selected or clipboard is empty.")
                continue
            
            response = self.process_input(user_input, text)
            if response:
                print(f"\n{response}")
            else:
                print("Failed to generate a summary or response.")

    def process_input(self, user_input, text):
        # Look up the corresponding function in the command map
        command_func = self.command_map.get(user_input)
        
        if command_func:
            return command_func(text)
        else:
            print("Invalid choice. Please try again.")
            return None