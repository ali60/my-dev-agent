# My AI Agent: Chat-Driven Developer Assistant

An intelligent chat-based assistant that streamlines developer workflows through natural conversation and smart command shortcuts. Powered by Large Language Models (LLMs) like OpenAI's GPT and Amazon Bedrock with real-time streaming markdown responses.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Smart Command System](#smart-command-system)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

My AI Agent transforms developer productivity through a **natural chat interface** combined with **smart command shortcuts**. Instead of rigid menu systems, you can:

🗣️ **Chat naturally** - Ask questions, get explanations, discuss code
⚡ **Use quick commands** - Invoke specific functions with `\s`, `\cr`, `\rw` etc.
📝 **See live responses** - Watch markdown-formatted answers stream in real-time
🧠 **Get smart suggestions** - Context-aware command recommendations

## Key Features

### 💬 **Natural Conversation Interface**
- Chat freely with AI about code, architecture, best practices
- No rigid command menus - type naturally and get intelligent responses
- Real-time streaming with beautiful markdown formatting

### ⚡ **Smart Command System**
- **Quick commands**: `\s` summarize, `\cr` code review, `\rw` reword text
- **Flexible input**: Use commands with inline text or clipboard content
- **Smart suggestions**: Get contextual command recommendations
- **Progressive disclosure**: Simple start, powerful when you need it

### 🎨 **Intelligent UI**
- **Contextual help**: Relevant suggestions based on your input
- **Autocomplete**: Live command completion as you type
- **Categorized commands**: Organized by Text, Code, Chat, and Utils
- **Visual feedback**: Rich formatting and clear status indicators

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API keys** in `.env`:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   ```

3. **Start chatting**:
   ```bash
   python capture.py
   ```

4. **Try it out**:
   ```
   > Hello! How do I implement a binary search?
   > \s Please summarize this document: [paste your text]
   > \cr def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)
   ```

## Usage Examples

### 🗣️ **Natural Conversation**
```bash
> How do I optimize this SQL query?
> What's the difference between REST and GraphQL?
> Can you explain microservices architecture?
```

### ⚡ **Quick Commands**
```bash
# Summarize text (from clipboard)
> \s

# Summarize with inline text
> \s Machine learning is a subset of artificial intelligence...

# Code review
> \cr def hello_world(): print("Hello, World!")

# Rewrite for professionalism
> \rw hey what's up → make this professional

# Generate unit tests
> \uc def add(a, b): return a + b
```

### 🔄 **Mixed Usage**
```bash
> Hi there! I'm working on a Python project
> \cr class Calculator: def add(self, a, b): return a + b
> Thanks! Can you also explain why unit testing is important?
> \uc def multiply(a, b): return a * b
```

## Smart Command System

### 📝 **Available Commands**

| Command | Function | Example |
|---------|----------|---------|
| `\s` | **Summarize** | `\s Please summarize this document` |
| `\r` | **General Response** | `\r Explain this concept` |
| `\cr` | **Code Review** | `\cr def hello(): print("world")` |
| `\rw` | **Reword Text** | `\rw make this more professional` |
| `\c` | **Critical Analysis** | `\c What are the issues here?` |
| `\rc` | **Rewrite Code** | `\rc improve this function` |
| `\uc` | **Unit Tests** | `\uc test this function` |
| `\lt` | **List Typos** | `\lt Check this text for errors` |
| `\sr` | **Security Review** | `\sr Check for vulnerabilities` |

### 🎯 **Smart Features**

#### **Progressive Disclosure**
- **Quick start**: See only essential commands initially
- **Full reference**: Type `help` for complete command list
- **Categorized view**: Commands organized by purpose

#### **Contextual Suggestions**
- **Smart recommendations**: Get relevant commands based on your input
- **Example**: Type "review code" → suggests `\cr`, `\uc`, `\sr`

#### **Autocomplete**
- **Live completion**: Type `\c` → see `\c` and `\cr` options
- **Reduces errors**: Prevents typos in command names

#### **Flexible Input**
- **Inline text**: `\s This is the text to summarize`
- **Clipboard fallback**: `\s` (uses clipboard when no text provided)
- **Natural mixing**: Combine commands and conversation seamlessly

## Architecture

The project follows a modular architecture with these key components:

- **Models Layer**: Handles interactions with LLMs (OpenAI GPT, Amazon Bedrock)
- **Service Layer**: Manages prompts, text processing, and clipboard interactions
- **Tasks Layer**: Implements specific automation tasks and workflows
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
   git clone https://github.com/yourusername/my-ai-agent.git
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

## Configuration

The application is configured through:

1. **Environment Variables**: Set in `.env` file for sensitive information
2. **Configuration Files**: `configuration/config.json` for application settings
3. **Model Configuration**: Settings for different LLM providers in the models directory

## Project Structure

```
my-ai-agent/
├── capture.py               # Main chat interface with smart commands
├── configuration/           # Configuration settings and environment handling
├── models/                  # LLM integration (OpenAI, Bedrock)
├── service/                 # Core services (prompt management, text processing)
│   ├── live_markdown_processor.py  # Real-time markdown streaming
│   └── utils/               # Utility functions for services
├── tasks/                   # Task-specific implementations
│   ├── aws/                 # AWS-specific tasks
│   ├── code_quality_checker.py     # Code analysis tools
│   ├── generate_unit_test.py       # Unit test generation
│   └── github_pr_review.py         # GitHub PR review automation
├── web/                     # Web interface components
│   ├── frontend/            # React-based frontend
│   └── backend/             # Flask/FastAPI backend
├── tests/                   # Unit and integration tests
├── .env                     # Environment variables (not in repo)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Interface Examples

### 🎨 **Smart Help System**

When you start the agent, you'll see a clean, focused interface:

```
🤖 AI Agent Help
⚡ Quick Commands:
  \s   summarize
  \r   response  
  \cr  code review
  \rw  reword

💡 Tips:
  • Type naturally for conversation
  • Use \<cmd> for specific functions
  • Type 'help' for all commands
```

### 🔍 **Contextual Suggestions**

The system provides smart suggestions based on your input:

```
> I need to review this code for security issues

🔍 Smart Suggestions
Based on 'I need to review this code for...'
💡 Suggested commands:
  \cr code review
  \uc generate unit test
  \sr security review
```

### ⚡ **Live Autocomplete**

Get instant feedback as you type commands:

```
> \c
⚡ Autocomplete
\c → critical response
\cr → code review
```

### 📖 **Full Command Reference**

Type `help` to see all commands organized by category:

```
📝 Text        💻 Code         💬 Chat        🔧 Utils
\s  summarize  \rc rewrite     \r  response   \n  null
\rw reword     \uc unit test   \c  critical
\lt typos      \cr review
               \sr security
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