# Automating Developers' Everyday Tasks

An open-source solution to streamline and automate routine tasks for developers using Scripts, Retrieval-Augmented Generation (RAG) with OpenSearch, and Large Language Models (LLMs) like OpenAI's GPT or Amazon Bedrock.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Scripts Layer](#scripts-layer)
  - [RAG Layer](#rag-layer)
  - [LLM Layer](#llm-layer)
- [Examples](#examples)
- [Configuration](#configuration)
  - [OpenSearch Setup](#opensearch-setup)
  - [LLM Configuration](#llm-configuration)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Overview

This project aims to automate developers' everyday tasks by integrating:

1. **Scripts Layer**: Automate basic tasks like cloning repositories.
2. **RAG Layer**: Use OpenSearch for storing and searching source code.
3. **LLM Layer**: Generate code and documentation using OpenAI or Amazon Bedrock.

## Features

- **Automate Git operations**: Clone, pull, and manage repositories via scripts.
- **Semantic Code Search**: Index and search codebases using OpenSearch.
- **Code Generation**: Generate code snippets and documentation with LLMs.
- **Extensible Architecture**: Modular design allows easy addition of new features.

## Technology Stack

- **Programming Language**: Python 3.7+
- **Scripts Layer**: Shell scripts and Python
- **RAG Layer**:
  - **Search Engine**: [OpenSearch](https://opensearch.org/)
  - **Embeddings**: [Sentence Transformers](https://www.sbert.net/)
- **LLM Layer**:
  - **OpenAI GPT-3/4**: [OpenAI API](https://openai.com/api/)
  - **Amazon Bedrock**: [AWS Bedrock](https://aws.amazon.com/bedrock/)
- **Package Management**: `pip` or `conda`
- **Environment Management**: `venv` or `conda`

## Prerequisites

- **Python**: Version 3.7 or higher
- **Git**: For repository management
- **Docker**: For running OpenSearch (optional but recommended)
- **OpenAI API Key**: If using OpenAI
- **AWS Credentials**: If using Amazon Bedrock
- **OpenSearch**: Local or hosted instance

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the project root directory:

   ```bash
   touch .env
   ```

   Add the following lines to `.env`:

   ```
   OPENAI_API_KEY=your_openai_api_key
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_REGION=your_aws_region
   OPENSEARCH_HOST=localhost
   OPENSEARCH_PORT=9200
   ```

5. **Set Up OpenSearch**

   If you don't have OpenSearch running, you can start a local instance using Docker:

   ```bash
   docker run -p 9200:9200 -e "discovery.type=single-node" opensearchproject/opensearch:latest
   ```

## Usage

### Scripts Layer

#### Clone a Repository

Use the script to clone a Git repository:

```bash
python scripts/clone_repo.py --repo_url https://github.com/example/repo.git
```

### RAG Layer

#### Index the Codebase

TODO

#### Search the Codebase

TODO

### LLM Layer

#### Generate Code or Diffrent LLM tasks

Generate code snippets or documentation using LLMs:

```bash
python capture

Press 's' to capture and summarize the selected text, or 'q' to quit.
[s:summarize, c: critical response, r: response, rc:rewrite_code, uc:generate unit test]

```

#### Bulk Generate unit test for python

```bash
python tasks/generate_unit_test.py

```


## Configuration

### OpenSearch Setup


### LLM Configuration

- **OpenAI**:
  - Sign up for an API key [here](https://platform.openai.com/account/api-keys).
  - Ensure `OPENAI_API_KEY` is set in your `.env` file.

- **Amazon Bedrock**:
  - Set up AWS credentials with access to Bedrock.
  - Ensure `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` are set in your `.env` file.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Project**

   Click on the 'Fork' button at the top right corner of the page.

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   Go to your fork on GitHub and open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenSearch**: For powerful search capabilities.
- **OpenAI and Amazon Bedrock**: For advanced language models.
- **Sentence Transformers**: For efficient embeddings.
- **Community Contributors**: Thanks for your valuable input and support.

## Contact

For questions or support, please open an issue or reach out via email:

- **Email**: [your.email@example.com](mailto:your.email@example.com)
- **GitHub Issues**: [Issue Tracker](https://github.com/yourusername/yourproject/issues)




## High level actions
1. Review a PR
2. Ask questions regards a repo
3. Chat about a certain design doc