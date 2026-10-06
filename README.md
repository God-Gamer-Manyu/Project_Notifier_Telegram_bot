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

## b. Configure a Destination (Channel or User)
You can send notifications to a channel (recommended) or directly to users.

### Option 1: Using a Telegram Channel (Recommended)
1. **Create a Channel**: In Telegram, create a new Public or Private channel.

2. **Add Bot as Admin:** Go to your Channel Info -> Administrators -> Add Admin. Search for your bot's username and add it. It only needs the Post Messages permission. This step is mandatory.

3. **Get the Channel ID:**

    - For a Public Channel: The ID is its username (e.g., `@my_awesome_channel`).

    - For a Private Channel: Post a message in the channel, forward it to `@userinfobot`, and find the `id` in the `forward_from_chat` section of the reply. It will be a long negative number (e.g., `-1001234567890`).

### Option 2: Get Your Chat ID
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
# You can mix and match channel and multiple user IDs, separated by commas
export TELEGRAM_NOTIFIER_ALLOWED_IDS="@my_public_channel,-1001234567890,987654321"
```

To make these permanent, add them to your `~/.bashrc`, `~/.zshrc`, or `~/.profile` file.

**On Windows:**
Open Command Prompt and run these commands:

```shell
set TELEGRAM_NOTIFIER_BOT_TOKEN="12345:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
set TELEGRAM_NOTIFIER_ALLOWED_IDS="@my_public_channel,-1001234567890,987654321"
```

To set them permanently, search for "Edit the system environment variables" in the Start Menu.

# 2. Installation
## Using the release package
Download the `.wheel` file from the release section and install the package using pip:
```shell
pip install "path to .wheel file"
```

## using the source code
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
    notifier = TelegramNotifier()
    await notifier.notify("The simulation has started.", level=1)
    # ... your code ...
    await notifier.notify("The task is complete!", level=1)

if __name__ == "__main__":
    asyncio.run(my_long_running_task())
```

Simpler Usage

```python
from notifier_pkg import TelegramNotifier
import asyncio

# ... your code ...

notifier = TelegramNotifier()
asyncio.run(notifier.notify("Deployment complete.", level=1))
```

Simpler Usage in synchronous event loop (e.g., Jupyter notebooks)

```python
from notifier_pkg import TelegramNotifier
import nest_asyncio

nest_asyncio.apply()

# ... your code ...

notifier = TelegramNotifier()
await notifier.notify("Deployment complete.", level=1)
```


Now, whenever you run `your_project_script.py`, it will send notifications to the users you configured!

---

# 4. Architecture & Concepts

```
Your Python project
   │  await notifier.notify("msg", level=1|2|3)
   ▼
TelegramNotifier (src/notifier_pkg/notifier.py)
   ├── reads TELEGRAM_NOTIFIER_BOT_TOKEN / TELEGRAM_NOTIFIER_ALLOWED_IDS from environment
   ├── validates level → emoji-prefixed Info / Warning / Error message
   └── fans out asynchronously to every allowed chat / channel ID
   ▼
Telegram Bot API (python-telegram-bot) ──► users & channels
```

- **Packaging:** `src/` layout, declarative `setup.cfg` + `pyproject.toml` (setuptools build backend), version and author exposed from `notifier_pkg/__init__.py`.
- **CI/CD:** the GitHub Actions workflow `build_and_release.yml` runs on every `v*.*.*` tag. It builds the wheel and sdist and attaches them to a **GitHub Release** automatically.
- **Security:** secrets come only from environment variables, and an allow-list of recipient IDs restricts who receives messages.

**Concepts:** asynchronous programming (`asyncio`) · Telegram Bot API integration · Python packaging and distribution (wheel / sdist) · environment-based configuration · structured logging and error handling · CI/CD release automation with **GitHub Actions**

# 5. Tech Stack

`Python 3.8+` · `asyncio` · `python-telegram-bot` · `setuptools` · `GitHub Actions`

# 👤 Author

**Rtamanyu N J**, [@God-Gamer-Manyu](https://github.com/God-Gamer-Manyu)
