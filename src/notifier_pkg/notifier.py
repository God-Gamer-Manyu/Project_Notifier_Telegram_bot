# File: src/notifier_pkg/notifier.py

import os
import asyncio
import logging
from typing import List

# We will use the python-telegram-bot library, which is a popular choice.
# It will be installed automatically via the setup.cfg file.
import telegram
from telegram.error import TelegramError

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TelegramNotifier:
    """
    A class to handle sending notifications to a pre-defined list of
    Telegram users.

    Reads the bot token and allowed chat IDs from environment variables.
    """
    def __init__(self):
        """
        Initializes the bot and checks for required environment variables.
        """
        logger.info("Initializing TelegramNotifier...")
        
        # --- Configuration ---
        # It's best practice to get secrets like API tokens from environment variables
        # rather than hardcoding them in the script.
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        allowed_ids_str = os.getenv("TELEGRAM_ALLOWED_IDS")

        if not self.bot_token:
            logger.error("FATAL: TELEGRAM_BOT_TOKEN environment variable not set.")
            raise ValueError("TELEGRAM_BOT_TOKEN is not configured.")

        if not allowed_ids_str:
            logger.error("FATAL: TELEGRAM_ALLOWED_IDS environment variable not set.")
            raise ValueError("TELEGRAM_ALLOWED_IDS is not configured.")

        # --- Process Allowed Chat IDs ---
        # The environment variable should be a comma-separated string of numbers.
        # e.g., "12345678,87654321"
        try:
            self.allowed_chat_ids: List[int] = [int(chat_id.strip()) for chat_id in allowed_ids_str.split(',')]
            if not self.allowed_chat_ids:
                raise ValueError
            logger.info(f"Notifier configured for {len(self.allowed_chat_ids)} user(s).")
        except (ValueError, AttributeError):
            logger.error(f"FATAL: TELEGRAM_ALLOWED_IDS is not a valid comma-separated list of numbers: '{allowed_ids_str}'")
            raise ValueError("Invalid format for TELEGRAM_ALLOWED_IDS.")

        # --- Initialize the Bot ---
        # The modern python-telegram-bot library is asynchronous.
        self.bot = telegram.Bot(token=self.bot_token)
        logger.info("Telegram Bot initialized successfully.")

    async def notify(self, message: str, level: int = 1):
        """
        Sends a message to all subscribed and allowed users.
        
        # Example usage when imported in another file:
        # from notifier_pkg.notifier import TelegramNotifier
        # import asyncio
        #
        # async def send_notification():
        #     notifier = TelegramNotifier()
        #     await notifier.notify("Hello from another module!", level=1)
        #
        # asyncio.run(send_notification())

        Args:
            message (str): The core message text to send.
            level (int): The risk/importance level of the message.
                         1: Info (default)
                         2: Warning
                         3: Error
        """
        if not isinstance(level, int) or level not in [1, 2, 3]:
            logger.warning(f"Invalid notification level '{level}'. Defaulting to 1 (Info).")
            level = 1

        # --- Format Message based on Level ---
        # Emojis help messages stand out in the chat.
        prefix = ""
        if level == 1:
            prefix = "ℹ️ [INFO]"
        elif level == 2:
            prefix = "⚠️ [WARNING]"
        elif level == 3:
            prefix = "❌ [ERROR]"
            
        full_message = f"{prefix}\n\n{message}"
        
        logger.info(f"Sending notification (Level {level}) to {len(self.allowed_chat_ids)} users.")

        # --- Send to all users concurrently ---
        # Create a list of tasks to run them in parallel.
        tasks = [
            self._send_single_message(chat_id, full_message) 
            for chat_id in self.allowed_chat_ids
        ]
        # asyncio.gather runs all tasks and waits for them to complete.
        await asyncio.gather(*tasks)
        logger.info("All notifications sent.")

    async def _send_single_message(self, chat_id: int, text: str):
        """
        A helper function to send a message to a single chat ID with error handling.
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
            logger.info(f"Successfully sent message to chat_id: {chat_id}")
        except TelegramError as e:
            # This can happen if the user has blocked the bot or the chat_id is wrong.
            logger.error(f"Failed to send message to chat_id {chat_id}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending to {chat_id}: {e}")

async def main():
    """
    An example of how to use the TelegramNotifier class.
    This function will only run if you execute this script directly.
    """
    print("--- Running Notifier Example ---")
    try:
        notifier = TelegramNotifier()
        
        # Example notifications
        await notifier.notify(
            "The simulation has completed successfully.\nFinal score: *98.7%*",
            level=1
        )
        await notifier.notify(
            "Disk space is running low on the server.\nUsage: *91%*",
            level=2
        )
        await notifier.notify(
            "A critical error occurred in the data processing module.\n`Process failed with exit code 1.`",
            level=3
        )
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # To run this example, make sure you have set the environment variables first.
    # Then run `python -m src.notifier_pkg.notifier` from the root directory.
    asyncio.run(main())
