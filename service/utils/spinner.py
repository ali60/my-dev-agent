import sys
import time
import threading
from contextlib import contextmanager


class Spinner:
    """A simple spinner class for showing progress"""
    
    SPINNERS = {
        'default': ['|', '/', '-', '\\'],
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
        'clock': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'bounce': ['⠁', '⠂', '⠄', '⠂'],
    }
    
    def __init__(self, message="Loading", spinner_type="default", delay=0.1):
        self.message = message
        self.spinner_chars = self.SPINNERS.get(spinner_type, self.SPINNERS['default'])
        self.delay = delay
        self.running = False
        self.thread = None
    
    def _spin(self):
        """Internal method to handle the spinning animation"""
        idx = 0
        while self.running:
            char = self.spinner_chars[idx % len(self.spinner_chars)]
            sys.stdout.write(f'\r{char} {self.message}')
            sys.stdout.flush()
            time.sleep(self.delay)
            idx += 1
    
    def start(self):
        """Start the spinner"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._spin)
            self.thread.daemon = True
            self.thread.start()
    
    def stop(self):
        """Stop the spinner"""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
            sys.stdout.flush()


@contextmanager
def spinning_cursor(message="Loading", spinner_type="default", delay=0.1):
    """Context manager for showing a spinner"""
    spinner = Spinner(message, spinner_type, delay)
    try:
        spinner.start()
        yield spinner
    finally:
        spinner.stop()


def show_spinner(message="Loading", duration=2, spinner_type="default"):
    """Show a spinner for a specific duration"""
    with spinning_cursor(message, spinner_type):
        time.sleep(duration)
