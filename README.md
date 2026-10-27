# TelegramPOC

A simple Python listener that watches one or two Telegram channels and writes every new message to a log file.

It uses [Telethon](https://docs.telethon.dev/), which logs in as **your Telegram user account**. No bot is needed, and it can read any channel your account has joined.

## Project structure

```
TelegramPOC/
├── main.py                    # Entry point: logging setup + channel listener
├── Telegram/
│   └── TelegramHelper.py      # Thin wrapper around the Telethon client
├── requirements.txt
├── .env.example               # Template for your .env
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- A Telegram account that has joined the channel(s) you want to watch
- Telegram API credentials (`api_id` and `api_hash`)

### Get your Telegram API credentials

1. Sign in at <https://my.telegram.org> with your phone number.
2. Open **API development tools**.
3. Create an application (any name and short name will do).
4. Copy the **App api_id** and **App api_hash**.

## Installation

```powershell
# 1. Clone the repo and go into it
git clone <repo-url>
cd TelegramPOC

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env from the template, then edit it
copy .env.example .env          # Windows
# cp .env.example .env          # Linux / macOS
```

## Configuration (`.env`)

| Variable                   | Required | Description                                                        |
|----------------------------|----------|--------------------------------------------------------------------|
| `TELEGRAM_API_ID`          | Yes      | Numeric api_id from my.telegram.org                                |
| `TELEGRAM_API_HASH`        | Yes      | api_hash from my.telegram.org                                      |
| `TELEGRAM_CHANNEL_ID`      | Yes      | Numeric ID of the channel to listen to (usually `-100...`)         |
| `TELEGRAM_TEST_CHANNEL_ID` | No       | Optional second channel. Leave empty to disable it                 |
| `LOG_FOLDER`               | No       | Folder for log files. Defaults to `logs` and is created if missing |

### Finding a channel ID

Forward any post from the channel to [@userinfobot](https://t.me/userinfobot), or open the channel in Telegram Web: the number in the URL (`https://web.telegram.org/a/#-100XXXXXXXXXX`) is the ID.

## Run

```powershell
python main.py
```

On the **first run**, Telethon asks for your phone number, the login code Telegram sends you and your 2FA password (if you set one). It then saves the session to `rk_session.session` in the project folder, so later runs start without asking.

> Keep `rk_session.session` private. Anyone who has it can use your Telegram account. It is already listed in `.gitignore`.

Press `Ctrl+C` to stop.

## Logs

Log files are written to `LOG_FOLDER`, and a new file starts each day:

| File                      | Contents                                      |
|---------------------------|-----------------------------------------------|
| `telegram_YYYYMMDD.log`   | Only the Telegram messages and listener events |
| `app_YYYYMMDD.log`        | Everything, including the Telegram messages and any errors |

Each line in `telegram_YYYYMMDD.log` looks like this:

```
2026-10-27 10:15:02,345 - telegram - INFO - [-1001234567890] 2026-10-27 04:45:01 | message text...
```
step 1 
Please enter your phone (or bot token): +919003467461
step 2
Please enter the code you received : 
The second timestamp is the time Telegram gives for the message, in UTC.

## Troubleshooting

- **No messages appear:** make sure your account has joined the channel and that the channel ID is correct, including the `-100` prefix.
- **`TELEGRAM_API_ID or TELEGRAM_API_HASH not set`:** check that `.env` is in the project folder and has those keys filled in.
- **Login problems:** delete `rk_session.session` and run again to log in from scratch.
