# bridge.py
from kiteconnect import KiteConnect
import telebot
import os
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


# ======= ACCOUNT SETTINGS =======

ACCOUNTS = [
{
 "name": "ACC1",
 "api_key": os.getenv("API_KEY_1"),
 "access_token": os.getenv("ACCESS_TOKEN_1"),
 "qty": 65
},
{
 "name": "ACC2",
 "api_key": os.getenv("API_KEY_2"),
 "access_token": os.getenv("ACCESS_TOKEN_2"),
 "qty": 130
}
]


# Kite Objects
KITES = []

for a in ACCOUNTS:
    k = KiteConnect(api_key=a["api_key"])
    k.set_access_token(a["access_token"])

    KITES.append({
        "kite": k,
        "qty": a["qty"],
        "name": a["name"]
    })



# ======= MESSAGE PARSER =======

def parse_message(text):

    symbol = None
    side = None

    # Symbol
    m = re.search(r"Order Details:\s*([A-Z0-9]+)", text)
    if m:
        symbol = m.group(1)

    # Side
    if "Transaction: BUY" in text:
        side = "BUY"
    elif "Transaction: SELL" in text:
        side = "SELL"

    return symbol, side



# ======= ORDER FUNCTION =======

def place(kite, symbol, side, qty):

    try:
        oid = kite.place_order(
            variety="regular",
            exchange="NFO",
            tradingsymbol=symbol,
            transaction_type=side,
            quantity=qty,
            order_type="MARKET",
            product="MIS"
        )

        return f"SUCCESS → {oid}"

    except Exception as e:
        return f"ERROR → {e}"



# ======= TELEGRAM LISTENER =======

@bot.message_handler(func=lambda m: True)
def handler(message):

    text = message.text

    # HutAlerts message જ process કરવું
    if "Order Details" not in text:
        return


    symbol, side = parse_message(text)

    if not symbol or not side:
        bot.reply_to(message, "❌ Parsing Failed")
        return


    report = f"📌 {symbol} | {side}\n\n"

    for k in KITES:

        res = place(
            k["kite"],
            symbol,
            side,
            k["qty"]
        )

        report += f"{k['name']} ({k['qty']}) → {res}\n"


    bot.reply_to(message, report)



print("Bridge Started...")
bot.infinity_polling()
