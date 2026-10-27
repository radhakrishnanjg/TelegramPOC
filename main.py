# main.py

import asyncio
import logging
import os
import sys
from datetime import date

from dotenv import load_dotenv

from Telegram.TelegramHelper import TelegramHelper


# -----------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------
def _file_handler(prefix: str) -> logging.FileHandler:
    log_folder = os.getenv("LOG_FOLDER", "logs")
    os.makedirs(log_folder, exist_ok=True)
    file_path = os.path.join(log_folder, f"{prefix}_{date.today().strftime('%Y%m%d')}.log")
    fh = logging.FileHandler(file_path, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    return fh


def setup_logging():
    """Root logger -> console + app_YYYYMMDD.log. 'telegram' logger -> telegram_YYYYMMDD.log (and app log)."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    root.addHandler(console)
    root.addHandler(_file_handler("app"))

    tg_log = logging.getLogger("telegram")
    tg_log.setLevel(logging.INFO)
    tg_log.addHandler(_file_handler("telegram"))


# -----------------------------------------------------------------
# TELEGRAM
# -----------------------------------------------------------------
def handle_message(data):
    tg_log = logging.getLogger("telegram")
    tg_log.info(f"[{data['CHANNELID']}] {data['timestamp']:%Y-%m-%d %H:%M:%S} | {data['message']}")


async def main():
    tg_log = logging.getLogger("telegram")
    api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
    api_hash = os.getenv("TELEGRAM_API_HASH", "")
    channel_ids = [
        int(c) for c in (os.getenv("TELEGRAM_CHANNEL_ID"), os.getenv("TELEGRAM_TEST_CHANNEL_ID")) if c
    ]

    if not api_id or not api_hash:
        tg_log.error("TELEGRAM_API_ID or TELEGRAM_API_HASH not set in .env — aborting.")
        return
    if not channel_ids:
        tg_log.error("TELEGRAM_CHANNEL_ID not set in .env — aborting.")
        return

    tg = TelegramHelper(api_id, api_hash)
    await tg.start()

    for channel_id in channel_ids:
        tg.listen_channelbyid(channel_id, handle_message)
        tg_log.info(f"Registered listener for channel {channel_id}")

    tg_log.info("Listening for new messages — press Ctrl+C to stop.")
    await tg.run()


if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopped manually.")
    except Exception as e:
        logging.exception(e)
