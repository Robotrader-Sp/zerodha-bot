# token_bot.py
from kiteconnect import KiteConnect
import pyotp
import telebot
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ACCOUNTS = [
{
 "name": "ACC1",
 "api_key": os.getenv("API_KEY_1"),
 "api_secret": os.getenv("API_SECRET_1"),
 "totp": os.getenv("TOTP_1")
},
{
 "name": "ACC2",
 "api_key": os.getenv("API_KEY_2"),
 "api_secret": os.getenv("API_SECRET_2"),
 "totp": os.getenv("TOTP_2")
}
]


def generate_token(acc):

    kite = KiteConnect(api_key=acc["api_key"])

    # TOTP generate
    otp = pyotp.TOTP(acc["totp"]).now()

    # અહીં તમે Zerodha login flow પ્રમાણે request_token આપશો
    session = kite.generate_session(
        request_token=os.getenv("REQUEST_TOKEN"),
        api_secret=acc["api_secret"]
    )

    return session["access_token"]



@bot.message_handler(commands=['token'])
def token_cmd(message):

    report = "🔐 TOKEN STATUS\n\n"

    for acc in ACCOUNTS:
        try:
            token = generate_token(acc)

            # Railway માં save (તમારું webhook હશે)
            requests.post(
                os.getenv("RAILWAY_URL"),
                json={
                    "account": acc["name"],
                    "token": token
                }
            )

            report += f"✅ {acc['name']} → SUCCESS\n"

        except Exception as e:
            report += f"❌ {acc['name']} → {str(e)}\n"


    bot.reply_to(message, report)


print("Token Bot Started...")
bot.infinity_polling()
