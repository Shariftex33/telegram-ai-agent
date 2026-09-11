
# Telegram AI Agent

A Python-based Telegram bot that uses a local AI model through Ollama to analyze Telegram channel posts.

## Features

* Telegram bot integration
* Local AI processing with Ollama
* Automatic analysis of Telegram channel posts
* Python-based implementation

## Requirements

* Python 3.x
* Ollama
* Telegram Bot Token

## Installation

Clone the repository:

```bash
git clone https://github.com/Shariftex33/telegram-ai-agent.git
cd telegram-ai-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file and add your Telegram bot token.

Do not upload the `.env` file to GitHub.

## Running the Bot

```bash
python telegram_bot.py
```

## Project Structure

```text
telegram-ai-agent/
├── agent.py
├── telegram_bot.py
├── test_agent.py
├── requirements.txt
├── README.md
└── .gitignore
```
