from telethon import TelegramClient, events
import logging

tg_log = logging.getLogger('telegram')


class TelegramHelper:
    def __init__(self, api_id: int, api_hash: str, session_name: str = "rk_session"):
        self.client = TelegramClient(session_name, api_id, api_hash)

    async def start(self):
        await self.client.start()
        tg_log.info("Telegram client started successfully")

    def listen_channelbyid(self, CHANNELID: int, callback):
        @self.client.on(events.NewMessage(chats=CHANNELID))
        async def handler(event):
            try:
                message = event.message.message
                if message:
                    callback({
                        "CHANNELID": CHANNELID,
                        "message": message,
                        "timestamp": event.message.date
                    })
            except Exception as e:
                tg_log.error(f"Error processing message: {e}")

    async def run(self):
        await self.client.run_until_disconnected()
