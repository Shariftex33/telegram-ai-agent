import os

from dotenv import load_dotenv

from telegram import Update

from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

from agent import analyze_post


# Load .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# --------------------------------
# Receive Telegram channel posts
# --------------------------------
async def handle_channel_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    post = update.channel_post

    if not post:
        return

    # Get text
    text = post.text

    # Some posts may contain captions instead
    if not text:
        text = post.caption

    if not text:
        print("Post has no text.")
        return

    # Don't analyze our own AI responses
    if text.startswith("🤖 AI Analysis"):
        return

    print("\n")
    print("=" * 60)
    print("NEW TELEGRAM POST")
    print("=" * 60)
    print(text)

    # --------------------------------
    # Analyze with Qwen
    # --------------------------------
    print("\nAnalyzing with Qwen...")

    result = analyze_post(text)

    # --------------------------------
    # Show result in terminal
    # --------------------------------
    print("\n")
    print("=" * 60)
    print("AI ANALYSIS")
    print("=" * 60)
    print(result)

    # --------------------------------
    # Send result back to same channel
    # --------------------------------
    try:
        await context.bot.send_message(
            chat_id=post.chat_id,
            text="🤖 AI Analysis\n\n" + result
        )

        print("\nAI analysis sent to Telegram!")

    except Exception as e:
        print("\nError sending result to Telegram:")
        print(e)


# --------------------------------
# Main
# --------------------------------
def main():

    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not found.")
        return

    print("Starting Telegram AI Agent...")

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Receive Telegram channel posts
    application.add_handler(
        MessageHandler(
            filters.ALL,
            handle_channel_post
        )
    )

    print("Bot is running...")
    print("Waiting for Telegram channel posts...")

    application.run_polling(
        allowed_updates=["channel_post"]
    )


# --------------------------------
# Start program
# --------------------------------
if __name__ == "__main__":
    main()