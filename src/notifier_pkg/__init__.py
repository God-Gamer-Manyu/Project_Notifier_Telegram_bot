# File: src/notifier_pkg/__init__.py

"""
Telegram Notifier Package

This package provides a simple, asynchronous class to send notifications
to a pre-defined list of Telegram users.
"""

# This makes the TelegramNotifier class available for import directly from the package.
# So you can do `from notifier_pkg import TelegramNotifier`
from .notifier import TelegramNotifier

__version__ = "1.0.0"
__author__ = "Rtamanyu N. J."
__email__ = "rtamanyu@gmail.com"