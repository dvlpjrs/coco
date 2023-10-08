import click
import os
import json
import platform
import pyperclip
from appdirs import user_data_dir
from InquirerPy import prompt
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from cocoai.api import CocoAPI

CONFIG_DIR = user_data_dir("coco", "coco")
CONFIG_FILE = f"{CONFIG_DIR}/config.json"


def load_api_key():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        return config.get("OPENAI_API_KEY")


def set_api_key(api_key):
    config = {"OPENAI_API_KEY": api_key}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


@click.command()
@click.argument("question", nargs=-1)
@click.option("-a", "--ask", is_flag=True, help="Question: ", type=str)
@click.option("-t", "--token", help="Reset OpenAI API Key", type=str)
def main(question, ask, token):
    if token:
        set_api_key(token)
        return

    api_key = load_api_key()

    if not api_key:
        api_key = click.prompt("Please enter OpenAI API Key", hide_input=True)
        set_api_key(api_key)

    if not question:
        question = click.prompt(f"Question").split()

    try:
        coco_api = CocoAPI(api_key)
        answers = coco_api.fetch_result(" ".join(question), platform.system())
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return

    if answers:
        answers.append(Choice(value=None, name="None of the above"))
        try:
            selected_answer = inquirer.select(
                message="Choose an option and press enter to copy to clipboard",
                choices=answers,
                default=answers[0],
            ).execute()
        except (KeyboardInterrupt, EOFError):
            click.echo("\nUser canceled the operation.")
            return

        if selected_answer == None:
            return
        pyperclip.copy(selected_answer)
        click.echo(selected_answer)
    else:
        click.echo("Sorry, I don't know how to answer that.")


if __name__ == "__main__":
    # Check if config directory/file exists, if not, create it
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)
    main()
