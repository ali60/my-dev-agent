from models.model_manager import ModelManager
from service.prompt_manager import PromptManager
from configuration.config import config


if __name__ == "__main__":
    try:
        model_manager = ModelManager(config)
        manager = PromptManager(config, model_manager=model_manager)
        manager.run()
    except KeyboardInterrupt:
        print("\nExiting...")