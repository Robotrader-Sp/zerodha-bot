from telethon import TelegramClient, events
import requests
import os

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats="@HotAlertsBot"))
async def handler(event):

    msg = event.raw_text

    # message Myzerodha_bot ને મોકલો
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

    print("Forwarded →", msg)


print("HotAlerts Listener Started...")
client.start()
client.run_until_disconnected()
