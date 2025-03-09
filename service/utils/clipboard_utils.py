# utils/clipboard_utils.py
import platform
import subprocess
import pyperclip
from rich import print as rprint


class ClipboardUtils:
    @staticmethod
    def copy_to_clipboard(text):
        """
        Copy text to clipboard based on platform
        """
        try:
            system = platform.system()

            if system == "Darwin":  # macOS
                try:
                    process = subprocess.Popen(
                        "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE
                    )
                    process.communicate(text.encode("utf-8"))
                    return True
                except Exception as e:
                    rprint(f"[red]Error using pbcopy: {e}[/red]")
                    return False

            elif system == "Linux":
                try:
                    process = subprocess.Popen(
                        ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
                    )
                    process.communicate(text.encode("utf-8"))
                    return True
                except Exception as e:
                    rprint(f"[red]Error using xclip: {e}[/red]")
                    return False

            else:  # Windows and fallback
                try:
                    pyperclip.copy(text)
                    return True
                except Exception as e:
                    rprint(f"[red]Error using pyperclip: {e}[/red]")
                    return False

        except Exception as e:
            rprint(f"[red]Error copying to clipboard: {e}[/red]")
            return False

    @staticmethod
    def paste_from_clipboard():
        """
        Paste text from clipboard based on platform
        """
        try:
            system = platform.system()

            if system == "Darwin":  # macOS
                try:
                    process = subprocess.Popen(
                        "pbpaste", stdout=subprocess.PIPE, env={"LANG": "en_US.UTF-8"}
                    )
                    output, _ = process.communicate()
                    return output.decode("utf-8")
                except Exception as e:
                    rprint(f"[red]Error using pbpaste: {e}[/red]")
                    return None

            elif system == "Linux":
                try:
                    process = subprocess.Popen(
                        ["xclip", "-selection", "clipboard", "-o"],
                        stdout=subprocess.PIPE,
                    )
                    output, _ = process.communicate()
                    return output.decode("utf-8")
                except Exception as e:
                    rprint(f"[red]Error using xclip: {e}[/red]")
                    return None

            else:  # Windows and fallback
                try:
                    return pyperclip.paste()
                except Exception as e:
                    rprint(f"[red]Error using pyperclip: {e}[/red]")
                    return None

        except Exception as e:
            rprint(f"[red]Error pasting from clipboard: {e}[/red]")
            return None
