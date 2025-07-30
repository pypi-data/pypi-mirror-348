import click
import os
import logging
from .errors import TeamXError

logger = logging.getLogger("TeamXBot.CLI")

@click.group()
def cli():
    """TeamXBot CLI for creating and managing bots."""
    pass

@cli.command()
@click.argument("name")
def create(name: str):
    """Create a new bot project with the given name."""
    try:
        os.makedirs(name)
        with open(f"{name}/bot.py", "w") as f:
            f.write("""
from team_x_og import TeamXBot, command

bot = TeamXBot("YOUR_BOT_TOKEN")

@command("start")
async def start_command(bot, update):
    chat_id = update["message"]["chat"]["id"]
    await bot.send_message(chat_id, "Hello, welcome to my bot!")

if __name__ == "__main__":
    bot.run()
            """)
        with open(f"{name}/requirements.txt", "w") as f:
            f.write("team_x_og>=0.1.0\n")
        logger.info(f"Created bot project: {name}")
        click.echo(f"Created bot project: {name}")
        click.echo(f"Run: cd {name} && pip install -r requirements.txt && python bot.py")
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        click.echo(f"Error creating project: {e}")

if __name__ == "__main__":
    cli()