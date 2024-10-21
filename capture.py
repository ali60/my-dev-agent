from service.prompt_manager import PromptManager
from configuration.config import config


if __name__ == "__main__":
    try:
        manager = PromptManager(config)
        manager.run()
    except KeyboardInterrupt:
        print("\nExiting...")