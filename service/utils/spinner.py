import sys
import time
import threading
import itertools
from contextlib import contextmanager

class Spinner:
    """
    A class that provides animated spinners to indicate processing or waiting.
    """
    
    def __init__(self, message="Processing", delay=0.1, spinner_type="dots"):
        """
        Initialize the spinner.
        
        Args:
            message (str): The message to display alongside the spinner
            delay (float): Time between spinner updates in seconds
            spinner_type (str): Type of spinner animation to use
        """
        self.message = message
        self.delay = delay
        self.running = False
        self.spinner_thread = None
        
        # Different spinner animation styles
        self.spinners = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "line": ["-", "\\", "|", "/"],
            "dots_simple": [".", "..", "..."],
            "arrow": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            "pulse": ["█", "▓", "▒", "░"],
            "bounce": ["⠁", "⠂", "⠄", "⠂"],
            "clock": ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"],
            "moon": ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"],
            "hearts": ["💖", "💗", "💓", "💞", "💕"],
            "stars": ["✶", "✸", "✹", "✺", "✹", "✷"],
        }
        
        self.spinner_chars = self.spinners.get(spinner_type, self.spinners["dots"])
    
    def spin(self):
        """The animation function that runs in a separate thread."""
        spinner_cycle = itertools.cycle(self.spinner_chars)
        while self.running:
            sys.stdout.write(f"\r{next(spinner_cycle)} {self.message}")
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write("\r\033[K")  # Clear the line
    
    def start(self):
        """Start the spinner animation."""
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()
    
    def stop(self):
        """Stop the spinner animation."""
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write("\r\033[K")  # Clear the line
        sys.stdout.flush()


@contextmanager
def spinning_cursor(message="Processing", spinner_type="dots"):
    """
    Context manager for using the spinner.
    
    Example:
        with spinning_cursor("Loading data..."):
            # Do some time-consuming operation
            time.sleep(5)
    """
    spinner = Spinner(message=message, spinner_type=spinner_type)
    spinner.start()
    try:
        yield
    finally:
        spinner.stop()


# Example usage if run directly
if __name__ == "__main__":
    print("Testing spinner animations:")
    
    for spinner_type in ["dots", "line", "dots_simple", "arrow", "pulse"]:
        print(f"\nTesting {spinner_type} spinner:")
        with spinning_cursor(f"Testing {spinner_type} spinner", spinner_type=spinner_type):
            time.sleep(3)
    
    print("\nAll spinner tests completed!")