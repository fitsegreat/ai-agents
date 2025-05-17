# AI Agents

This repository contains code and resources related to AI agents tool calling.


## Prerequsite
- Make sure [devbox](https://www.jetify.com/devbox) and [nix](https://nixos.org/) installed
- [Ollama](https://github.com/ollama/ollama/blob/main/docs/api.md) with [**qwen3:1.7b** model](https://ollama.com/library/qwen3:1.7b)
- [Google Gemini](https://ai.google.dev/gemini-api/docs/function-calling?example=weather) model with the necessary API key, If you want to run [Gemini](gemini.py) file.

## Instructions to run on local LLMs
1. Start the development environment
```sh
devbox shell
```
2. Make sure ollama is installed and the necessary model is available
```sh
ollama list

NAME          ID              SIZE      MODIFIED
gemma3:1b     8648f39daa8f    815 MB    50 minutes ago
qwen3:1.7b    458ce03a2187    1.4 GB    About an hour ago
qwen3:0.6b    3bae9c93586b    522 MB    2 hours ago
```
3. Run the `main.py`
```sh
uv run main.py
```
## Instructions to run on Google Gemini LLMs
1. Start the development environment
```sh
devbox shell
```
2. Rename `.env.example` to `.env` file and provide a valid API key
3. Run the `gemini.py`
```sh
uv run gemini.py
```