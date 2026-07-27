import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

BOT_TOKEN = os.getenv("8618805037:AAF0x9Nps9sePsuRK8XDMi9OrVxq69zM60k")

print("BOT_TOKEN =", BOT_TOKEN)
# Load products
def load_products():
    try:
        with open("products.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

products = load_products()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 ABMPF Inventory Bot\n\n"
        "Send:\n"
        "• Last 4-6 digits of a barcode\n"
        "Example:\n"
        "6171\n\n"
        "or send a product name\n"
        "Example:\n"
        "Biogesic"
    )


async def reload_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global products
    products = load_products()
    await update.message.reply_text(
        f"✅ Reload complete!\nLoaded {len(products)} products."
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global products

    query = update.message.text.strip().lower()

    results = []

    # Barcode search
    if query.isdigit():

        for item in products:
            barcode = str(item["barcode"])

            if barcode.endswith(query):
                results.append(item)

    else:
        # Product name search
        for item in products:
            if query in item["name"].lower():
                results.append(item)

    if len(results) == 0:
        await update.message.reply_text("❌ Product not found.")
        return

    if len(results) > 10:
        results = results[:10]

    message = ""

    for i, item in enumerate(results, start=1):

        message += (
            f"{i}. 🛒 {item['name']}\n"
            f"🏷 Barcode: {item['barcode']}\n"
            f"💰 Price: ₱{item['price']}\n\n"
        )

    await update.message.reply_text(message)


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reload", reload_data))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            search
        )
    )

    print("ABMPF Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
