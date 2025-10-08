# Telegram Notifier Package
A simple, asynchronous Python package to send notifications from your projects to a pre-defined list of Telegram users.

This is perfect for monitoring long-running tasks, such as machine learning training, data processing jobs, or server status alerts.

# Features
- Easy to integrate into any Python project.

- Restricted access: Only users you define can receive notifications.

- Three levels of notifications: Info, Warning, and Error.

- Asynchronous: Built with `asyncio` for modern, non-blocking performance.

- Simple configuration using environment variables.

# 1. Setup
## a. Create a Telegram Bot
1. Open Telegram and search for the **@BotFather** user (it has a blue checkmark).

2. Start a chat and send the `/newbot` command.

3. Follow the instructions to give your bot a name and a username.

4. **BotFather will give you an HTTP API token. Copy this token and save it** securely. This is your `TELEGRAM_BOT_TOKEN`.

## b. Get Your Chat ID
The bot needs to know who to send messages to. Each user has a unique Chat ID.

1. Search for the bot **@userinfobot** in Telegram.

2. Start a chat with it and it will immediately reply with your user information, including your **ID**.

3. If you want to add more people, have them do the same to get their own IDs.

## c. Set Environment Variables
This package reads the bot token and the list of allowed user IDs from environment variables. This is more secure than writing them directly in your code.

**On Linux or macOS:**
Open your terminal and run these commands, replacing the placeholder values with your actual token and ID(s).

```shell
export TELEGRAM_NOTIFIER_BOT_TOKEN="12345:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
# For multiple users, separate their IDs with a comma
export TELEGRAM_NOTIFIER_ALLOWED_IDS="123456789,987654321"
```

To make these permanent, add them to your `~/.bashrc`, `~/.zshrc`, or `~/.profile` file.

**On Windows:**
Open Command Prompt and run these commands:

```shell
set TELEGRAM_NOTIFIER_BOT_TOKEN="12345:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
set TELEGRAM_NOTIFIER_ALLOWED_IDS="123456789,987654321"
```

To set them permanently, search for "Edit the system environment variables" in the Start Menu.

# 2. Installation
Once you have placed all the files in a directory, navigate to that directory in your terminal and install the package locally using pip:

```shell
# The '.' means 'install from the current directory'
pip install .
```

This command will read the `setup.cfg` file, find the source code in the `src` folder, and install all the required dependencies (like `python-telegram-bot`).

# 3. Usage in Your Project
Here is how you can import and use the `TelegramNotifier` in any of your other Python projects after you've installed it.

```python
# your_project_script.py
import asyncio
from notifier_pkg import TelegramNotifier

async def my_long_running_task():
    print("Starting a complex task...")
    
    # Initialize the notifier
    notifier = TelegramNotifier()

    # --- Your code here ---
    # Simulate some work
    await asyncio.sleep(5) 
    
    # Send a notification when the task is done
    await notifier.notify(
        "Data processing is complete.\nProcessed 1.5M records.",
        level=1  # Info
    )

    # --- Simulate another task that fails ---
    try:
        print("Starting a task that might fail...")
        await asyncio.sleep(2)
        # Force an error for demonstration
        result = 10 / 0
    except Exception as e:
        # Send an error notification
        await notifier.notify(
            f"An error occurred in the task!\n\n*Details:*\n`{str(e)}`",
            level=3  # Error
        )

if __name__ == "__main__":
    # Since the notifier is async, you need an async entry point.
    asyncio.run(my_long_running_task())
```


Now, whenever you run `your_project_script.py`, it will send notifications to the users you configured!