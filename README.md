# My DEV Agent: Automating Developers' Everyday Tasks

An intelligent assistant that streamlines and automates routine development tasks using a combination of scripts, Retrieval-Augmented Generation (RAG) with OpenSearch, and Large Language Models (LLMs) like OpenAI's GPT and Amazon Bedrock.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Text Processing and Code Generation](#text-processing-and-code-generation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

My AI Agent is designed to boost developer productivity by automating common tasks and providing intelligent assistance through:

1. **Text and Code Processing**: Capture text/code from clipboard and generate summaries, critical responses, or code improvements
2. **AWS Integration**: Special tooling for AWS-related tasks like design reviews and security analysis
3. **Flexible LLM Support**: Seamlessly switch between OpenAI and Amazon Bedrock models

## Key Features

- **Smart Clipboard Integration**: Capture and process text directly from your clipboard
- **Multiple Response Types**: Generate summaries, critical analyses, code rewrites, and unit tests
- **AWS Workflow Support**: Tools for reviewing designs, handling CR comments, and security analysis
- **Modular Architecture**: Easily extend with new capabilities and model integrations
- **Configurable LLM Backend**: Use OpenAI GPT or Amazon Bedrock models based on your needs

## Architecture

The project follows a modular architecture with these key components:

- **Models Layer**: Handles interactions with LLMs (OpenAI GPT, Amazon Bedrock)
- **Service Layer**: Manages prompts, text processing, and clipboard interactions
- **Configuration Layer**: Centralizes settings and environment variables

## Prerequisites

- Python 3.7+
- Git
- OpenAI API key (if using OpenAI models)
- AWS credentials with Bedrock access (if using Amazon Bedrock)
- OpenSearch instance (for RAG capabilities)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/my-dev-agent.git
   cd my-ai-agent
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file with your API keys and configuration:

   ```
   OPENAI_API_KEY=your_openai_api_key
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   ```

## Usage

### Text Processing and Code Generation

The main entry point for the application is the `capture.py` script:

```python
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
```

To use the application:

```bash
python capture.py
```

This will start an interactive session where you can:
- Press 's' to summarize selected text
- Press 'c' for critical response
- Press 'r' for general response
- Press 'rc' to rewrite code
- Press 'uc' to generate unit tests
- Press 'q' to quit

## Configuration

The application is configured through:

1. **Environment Variables**: Set in `.env` file for sensitive information
2. **Configuration Files**: `configuration/config.json` for application settings
3. **Model Configuration**: Settings for different LLM providers in the models directory

## Project Structure

```
my-ai-agent/
├── configuration/       # Configuration settings and environment handling
├── models/              # LLM integration (OpenAI, Bedrock)
├── service/             # Core services (prompt management, text processing)
│   └── utils/           # Utility functions for services
├── tests/               # Unit and integration tests
├── .env                 # Environment variables (not in repo)
├── capture.py           # Main clipboard capture utility
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.