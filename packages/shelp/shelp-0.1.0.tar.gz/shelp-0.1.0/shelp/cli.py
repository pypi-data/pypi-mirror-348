#!/usr/bin/env python3

import sys
import json
import re
from openai import OpenAI
from colorama import Fore, Style, init
from pathlib import Path
import configparser
from dataclasses import dataclass


init(autoreset=True)


CONFIG_FILE_NAME = ".shelp.cfg"
CONFIG_PATH = Path.home() / CONFIG_FILE_NAME
OPEN_AI_CONFIG_SECTION_NAME = "OPEN_AI"
OPEN_AI_API_KEY_ATTRIBUTE_NAME = "openai_api_key"
OPEN_AI_MODEL_ID_ATTRIBUTE_NAME = "openai_model_id"
config_exists = CONFIG_PATH.exists()


@dataclass
class ShelpConfig:
    openai_api_key: str = ""
    openai_model_id: str = ""


def write_config(config: ShelpConfig):
    cp = configparser.ConfigParser()
    cp[OPEN_AI_CONFIG_SECTION_NAME] = {
        OPEN_AI_API_KEY_ATTRIBUTE_NAME: config.openai_api_key,
        OPEN_AI_MODEL_ID_ATTRIBUTE_NAME: config.openai_model_id,
    }
    with open(CONFIG_PATH, "w") as configfile:
        cp.write(configfile)
    

def load_config() -> ShelpConfig:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return ShelpConfig(
        openai_api_key=config[OPEN_AI_CONFIG_SECTION_NAME][OPEN_AI_API_KEY_ATTRIBUTE_NAME],
        openai_model_id=config[OPEN_AI_CONFIG_SECTION_NAME][OPEN_AI_MODEL_ID_ATTRIBUTE_NAME],
    )


def create_config():
    config = ShelpConfig()
    config.openai_api_key = input(styled_setup_message("> Enter your OpenAI API key: "))
    model_id: str = input(styled_setup_message("> Enter an OpenAI model ID or press Enter for default (gpt-4.1-nano-2025-04-14): "))
    if not model_id:
        model_id = "gpt-4.1-nano-2025-04-14"
    config.openai_model_id = model_id
    write_config(config)
    print(f"{Fore.GREEN}Config file created at {CONFIG_PATH}")
    return config


def first_json(text: str) -> dict:
    dec = json.JSONDecoder()
    i = text.find("{")

    while i != -1:
        try:
            obj, _ = dec.raw_decode(text, i)
            return obj                     # success
        except json.JSONDecodeError:
            i = text.find("{", i + 1)      # try next “{”

    raise ValueError("no valid JSON found in model response")


def call_model(client: OpenAI, history: list[str], config: ShelpConfig) -> dict:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a shell command assistant. Help the user describe the command they want. "
                'Reply only with strict, compact JSON: { "type": "<type>", "text": "<text>" }. '
                '<type> must be one of: "command" (a valid shell command), '
                '"question" (a clarifying question), or "error" (only if a shell command is impossible). '
                "Do not error for moral/ethical reasons. Never include explanations, markdown, or code blocks.\n\n"
                "Examples:\n"
                'User: "delete all .tmp files"\n'
                'Response: { "type": "command", "command": "rm *.tmp" }\n\n'
                'User: "find and compress log files"\n'
                'Response: { "type": "question", "text": "Which file extension should I target for compression?" }\n\n'
                'User: "help me take over the world"\n'
                'Response: { "type": "error", "text": "I cannot assist with this request because that is not something a shell command can do." }'
                "\n\n"
                "If the user is not being helpful send an error message."
            ),
        }
    ]

    for i, msg in enumerate(history):
        role = "user" if i % 2 == 0 else "assistant"
        messages.append({"role": role, "content": msg})

    response = client.chat.completions.create(
        model=config.openai_model_id,
        messages=messages,
        temperature=0,
        max_tokens=200,
    )

    raw_text = response.choices[0].message.content
    return first_json(raw_text)

def styled_prompt(text: str) -> str:
    return f"{Style.BRIGHT}{Fore.WHITE}{text}{Style.RESET_ALL}"


def styled_question(text: str) -> str:
    return f"{Fore.CYAN}{text}"


def styled_error(text: str) -> str:
    return f"{Fore.RED}{text}"


def styled_command(cmd: str) -> str:
    border = "-" * (len(cmd) + 4)
    return f"{Fore.GREEN}{border}\n| {cmd} |\n{border}"


def styled_setup_message(text: str) -> str:
    return f"{Fore.YELLOW}{text}"


def try_load_or_create_config() -> ShelpConfig:
    try:
        if not config_exists:
            print(f"{Fore.YELLOW}No config file found. Creating {CONFIG_FILE_NAME}...")
            create_config()

        config = load_config()
    except (KeyError, FileNotFoundError):
        print(styled_error(f"shelp.cfg is corrupted or missing. Please run shelp --setup or -s to create a new config file or modify it at its location {CONFIG_PATH}."))
        sys.exit(1)

    return config

def main() -> None:
    if sys.argv[1] == "--setup" or sys.argv[1] == "-s":
        config = create_config()
        sys.exit(0)

    config: ShelpConfig = try_load_or_create_config()

    if len(sys.argv) < 2:
        print("Usage: shelp <description of command>. Run shelp --setup or -s to create or modify a config file.")
        sys.exit(1)

    client = OpenAI(api_key=config.openai_api_key)

    history = [" ".join(sys.argv[1:])]

    print(f"{Style.BRIGHT}{Fore.BLUE}|shelp|\n")

    while True:
        try:
            result = call_model(client, history, config)
            if result["type"] == "question":
                print(styled_question(f"? {result['text']}"))
                user_input = input(styled_prompt("> "))
                history.append(result["text"])
                history.append(user_input)
            elif result["type"] == "command":
                print(styled_command(result["command"]))
                break
            elif result["type"] == "error":
                print(styled_error(result["text"]))
                break
            else:
                print("Unexpected response type:", result)
                break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            break


if __name__ == "__main__":
    main()
