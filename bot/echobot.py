#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


ANALYZE, TEXT_FILE = range(2)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    reply_keyboard = [["Analyze", "Text", "Other"]]
    user = update.effective_user
    presentation = rf"Hi! {user.first_name} My name is OpenLogsLauz Bot. I can analyze a few logs files"
    
    await update.message.reply_text(
        rf"{presentation}",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Analyze"
        )
    )
    return ANALYZE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def read_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user a read file."""
    await update.message.reply_text("Upload your log file!")
    attachment_file = await update.message.document.get_file()

    tmp_file = "tmp/attachment.txt"
    await attachment_file.download_to_drive(tmp_file)


    # read txt
    with open(tmp_file, 'r') as file:
        # Read the first line
        first_line = file.readline()

        # Call for openAI to reply with features


    await update.message.reply_document(tmp_file, caption=f"The first line: {first_line}")

    return TEXT_FILE

async def analyze_log() -> None:
    "Analyze a log and returns some features"

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_KEY).build()

    # Basic commands of start and help
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Command for openAI
    application.add_handler(CommandHandler("analyze_log", analyze_log))

    # Basic echo handler for files
    application.add_handler(
        MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, read_file, block=True)
    )

    # Add conversation handler with the states FUNCTION, TEXT
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ANALYZE: [MessageHandler(filters.Regex("^(Analyze|Analyse)$"), read_file)],
            TEXT_FILE: [MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, cancel)]
            #LOCATION: [
            #    MessageHandler(filters.LOCATION, location),
            #    CommandHandler("skip", skip_location),
            #],
            #BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )




    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()