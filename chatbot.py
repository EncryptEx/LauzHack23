import logging

from dotenv import load_dotenv
import os



from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from ai.gpt_core import askAnotherQuestion, askGPT, hardRestartConversation

load_dotenv()
TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


START, PROCESSED, AWAITING_USER, QUESTION, CLOSED, SECOND_QUESTION = range(6)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Yes"]]
    user = update.effective_user

    await update.message.reply_text(
        f"Hi! {user.first_name} My name is OpenLogsLauz. I will hold a conversation with you and analyze logs files that you send me"
        "\nSend /cancel to stop talking to me.\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Process file?"
        ),
    )

    return START

async def ask_for_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Upload your log file!")

    return PROCESSED

async def process_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user a read file."""


    attachment_file = await update.message.document.get_file()

    tmp_file = "tmp/attachment.txt"
    await attachment_file.download_to_drive(tmp_file)

    await update.message.reply_text(rf"Write your question!")
    
    #await get_an_answer(update, context)

    return QUESTION #answer question
    
async def get_an_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):    

    prompt_question = update.message.text

    tmp_file = "tmp/attachment.txt"
    response = askGPT(tmp_file, prompt_question)

    
    await update.message.reply_text(rf"The answer: {response}" + "\n\n Write your next question and press enter,")

    return AWAITING_USER


async def get_an_answer_two(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    
    prompt_question = update.message.text
    print(prompt_question)
    response = askAnotherQuestion(prompt_question)

    await update.message.reply_text(rf"The answer: {response}  " + "\n\n Write your next question and press enter, If you have no questions send /cancel")
    return AWAITING_USER

async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await update.message.reply_text("Write your question and press enter, \n if you have no questions send /cancel")
    #await update.message.reply_text(text=" \n If you have no questions send /cancel", reply_markup=ForceReply(selective=True))
    prompt_question = update.message.text
    print(prompt_question)
    response = askAnotherQuestion(prompt_question)
        
    await update.message.reply_text(rf"The answer: {response}  " + "\n\n Write your next question and press enter, If you have no questions send /cancel")

    return SECOND_QUESTION




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    hardRestartConversation()
    await update.message.reply_text(
        "Bye!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_KEY).build()

    # Add conversation handler with the states START, PROCESSED, AWAITING_USER, CLOSED
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(filters.Regex("^(Yes)$"), ask_for_file)],
            PROCESSED: [MessageHandler(filters.ALL, process_file), CommandHandler("cancel", cancel)],
            AWAITING_USER: [
                MessageHandler(filters.ALL, answer_question),
                CommandHandler("cancel", cancel)
            ],
            QUESTION : [MessageHandler(filters.ALL, get_an_answer), CommandHandler("cancel", cancel)],
            SECOND_QUESTION : [MessageHandler(filters.ALL, get_an_answer_two), CommandHandler("cancel", cancel)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()