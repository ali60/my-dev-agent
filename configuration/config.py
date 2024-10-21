import json

def load_config(config_path="configuration/config.json"):
    """Loads the configuration file and returns it as a dictionary."""
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding the config file: {e}")
        return None


config = load_config()
