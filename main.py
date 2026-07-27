import json
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("8164194572:AAEapgaypu-Wa5nMqhAFkcvfDGjSbN2yw3w")


def load_products():
    try:
        with open("products.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


products = load_products()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 ABMPF Inventory Bot\n\n"
        "Send the last 4-6 digits of the barcode.\n\n"
        "Example:\n"
        "6171\n\n"
        "You can also search by product name."
    )


async def reload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global products
    products = load_products()
    await update.message.reply_text(
        f"Reloaded {len(products)} products."
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip().lower()

    results = []

    if text.isdigit():

        for item in products:
            if str(item["barcode"]).endswith(text):
                results.append(item)

    else:

        for item in products:
            if text in item["name"].lower():
                results.append(item)

    if not results:
        await update.message.reply_text("❌ Product not found.")
        return

    msg = ""

    for item in results[:10]:
        msg += (
            f"🛒 {item['name']}\n"
            f"🏷 Barcode: {item['barcode']}\n"
            f"💰 Price: ₱{item['price']}\n\n"
        )

    await update.message.reply_text(msg)


def main():

    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN environment variable is missing!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reload", reload))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, search)
    )

    print("ABMPF Bot Started!")

    app.run_polling()


if __name__ == "__main__":
    main()