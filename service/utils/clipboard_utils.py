# service/utils/clipboard_utils.py
import subprocess
import platform
import time
import pyperclip


class ClipboardUtils:
    """Utility class for clipboard operations"""
    
    @staticmethod
    def get_selected_text():
        """
        Capture selected text by simulating Ctrl+C and then reading from clipboard
        """
        os_type = platform.system().lower()

        if os_type == "linux":
            # Use xdotool to simulate Ctrl+C on Linux
            subprocess.run(["xdotool", "key", "ctrl+c"])

        elif os_type == "darwin":  # macOS
            # Use AppleScript to simulate Cmd+C on macOS
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    'tell application "System Events" to keystroke "c" using {command down}',
                ]
            )

        elif os_type == "windows":
            # On Windows, simulate Ctrl+C using the built-in 'clip' functionality
            subprocess.run(["powershell.exe", "Get-Clipboard"], stdout=subprocess.PIPE)

        # Allow time for the clipboard to update
        time.sleep(0.1)

        # Get the clipboard content using pyperclip
        selected_text = pyperclip.paste()

        return selected_text
    
    @staticmethod
    def set_clipboard_text(text):
        """
        Set text to clipboard
        """
        pyperclip.copy(text)
    
    @staticmethod
    def get_clipboard_text():
        """
        Get text from clipboard without simulating key press
        """
        return pyperclip.paste()
    
    @staticmethod
    def paste_from_clipboard():
        """
        Alias for get_selected_text() for compatibility
        """
        return ClipboardUtils.get_selected_text()
    
    @staticmethod
    def copy_to_clipboard(text):
        """
        Copy text to clipboard (alias for set_clipboard_text)
        """
        return ClipboardUtils.set_clipboard_text(text)
