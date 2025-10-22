# File: src/notifier_pkg/notifier.py

import os
import asyncio
import logging
from typing import List, Union

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
    Telegram users or channels.

    Reads the bot token and allowed chat/channel IDs from environment variables.

    Examples:
        Basic usage (from an async context and running inside a synchronous event loop (e.g., Jupyter notebooks)):

        >>> from notifier_pkg import TelegramNotifier
    >>> import nest_asyncio
    >>> nest_asyncio.apply()
    >>> notifier = TelegramNotifier()
    >>> await notifier.notify("Deployment complete.", level=1)
    >>> await notifier.notify("High memory usage detected on server X.", level=2) # Sending a Warning

        Basic usage (from an async context and running inside a python file):

        >>> from notifier_pkg import TelegramNotifier
    >>> import asyncio
    >>> async def main():
    >>>     notifier = TelegramNotifier()
    >>>     await notifier.notify("Deployment complete.", level=1)

    Notes:
        - The final message format is "<prefix>\\n\\n<message>" where prefix is one of:
            "ℹ️ [INFO]", "⚠️ [WARNING]", "❌ [ERROR]".
        - The function logs the number of destinations before sending and logs when all
            notifications have been sent.
    """
    def __init__(self):
        """
        Initializes the bot and checks for required environment variables.
        """
        logger.info("Initializing TelegramNotifier...")
        
        self.bot_token = os.getenv("TELEGRAM_NOTIFIER_BOT_TOKEN")
        allowed_ids_str = os.getenv("TELEGRAM_NOTIFIER_ALLOWED_IDS")

        if not self.bot_token:
            logger.error("FATAL: TELEGRAM_NOTIFIER_BOT_TOKEN environment variable not set.")
            raise ValueError("TELEGRAM_NOTIFIER_BOT_TOKEN is not configured.")

        if not allowed_ids_str:
            logger.error("FATAL: TELEGRAM_NOTIFIER_ALLOWED_IDS environment variable not set.")
            raise ValueError("TELEGRAM_NOTIFIER_ALLOWED_IDS is not configured.")

        # --- Process Allowed Chat and Channel IDs ---
        # The environment variable should be a comma-separated string.
        # e.g., "@my_public_channel,-100123456789,12345678"
        try:
            # --- MODIFICATION ---
            # This logic now handles usernames (@channel), private channel IDs (-100...), and user IDs (123...)
            raw_ids = [chat_id.strip() for chat_id in allowed_ids_str.split(',')]
            self.allowed_chat_ids: List[Union[str, int]] = []
            for chat_id in raw_ids:
                if chat_id.startswith('@') or chat_id.startswith('-'):
                    self.allowed_chat_ids.append(chat_id) # Keep as string for channels
                else:
                    self.allowed_chat_ids.append(int(chat_id)) # Convert to int for users
            
            if not self.allowed_chat_ids:
                raise ValueError
            logger.info(f"Notifier configured for {len(self.allowed_chat_ids)} channel(s)/user(s).")
        except (ValueError, AttributeError):
            logger.error(f"FATAL: TELEGRAM_ALLOWED_IDS is not a valid comma-separated list of IDs: '{allowed_ids_str}'")
            raise ValueError("Invalid format for TELEGRAM_ALLOWED_IDS.")

        self.bot = telegram.Bot(token=self.bot_token)
        logger.info("Telegram Bot initialized successfully.")

    async def notify(self, message: str, level: int = 1):
        """
        Send a formatted notification message to all subscribed and allowed chats.
        This coroutine sends `message` to every chat ID listed in self.allowed_chat_ids.
        The function validates the provided `level`, maps it to a short emoji-prefixed
        status header, prepends that header to the message body, and dispatches the
        messages concurrently using asyncio.gather.
        
        Params:
            `message (str)`: The core text to send in the notification body.
            `level (int, optional)`: Importance/risk level of the message. Supported values:
               - 1 - Info (default)
               - 2 - Warning
               - 3 - Error

               If an invalid value is provided, the function logs a warning and defaults to 1.

        Returns:
            None
        Raises:
            `Exception`: Any exception raised by the underlying send tasks (self._send_single_message)
            will propagate from asyncio.gather. The first encountered exception is raised
            to the caller.
        Examples:
            Basic usage (from an async context and running inside a synchronous event loop (e.g., Jupyter notebooks)):

            >>> from notifier_pkg import TelegramNotifier
        >>> import nest_asyncio
        >>> nest_asyncio.apply()
        >>> notifier = TelegramNotifier()
        >>> await notifier.notify("Deployment complete.", level=1)
        >>> await notifier.notify("High memory usage detected on server X.", level=2) # Sending a Warning

            Basic usage (from an async context and running inside a python file):

            >>> from notifier_pkg import TelegramNotifier
        >>> import asyncio
        >>> async def main():
        >>>     notifier = TelegramNotifier()
        >>>     await notifier.notify("Deployment complete.", level=1)

        Notes:
            - The final message format is "<prefix>\\n\\n<message>" where prefix is one of:
              "ℹ️ [INFO]", "⚠️ [WARNING]", "❌ [ERROR]".
            - The function logs the number of destinations before sending and logs when all
              notifications have been sent.
        """
        if not isinstance(level, int) or level not in [1, 2, 3]:
            logger.warning(f"Invalid notification level '{level}'. Defaulting to 1 (Info).")
            level = 1

        prefix = ""
        if level == 1:
            prefix = "ℹ️ [INFO]"
        elif level == 2:
            prefix = "⚠️ [WARNING]"
        elif level == 3:
            prefix = "❌ [ERROR]"
            
        full_message = f"{prefix}\n\n{message}"
        
        logger.info(f"Sending notification (Level {level}) to {len(self.allowed_chat_ids)} destination(s).")

        tasks = [
            self._send_single_message(chat_id, full_message) 
            for chat_id in self.allowed_chat_ids
        ]
        await asyncio.gather(*tasks)
        logger.info("All notifications sent.")

    async def _send_single_message(self, chat_id: Union[str, int], text: str):
        """
        A helper function to send a message to a single chat ID with error handling.
        This function requires no changes, as the library handles both string and int IDs.
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
            logger.info(f"Successfully sent message to chat_id: {chat_id}")
        except TelegramError as e:
            logger.error(f"Failed to send message to chat_id {chat_id}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending to {chat_id}: {e}")

# The main function for testing remains the same.
async def main():
    print("--- Running Notifier Example ---")
    try:
        notifier = TelegramNotifier()
        await notifier.notify("This is a test notification to the configured channels and users.", level=1)
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

