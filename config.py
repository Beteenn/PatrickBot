import os
import logging


class DefaultConfig:

    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
