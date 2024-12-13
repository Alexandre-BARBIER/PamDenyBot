from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
import random
# On cree le bot qui permet de gerer l'api tg

TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(TOKEN)

denied_user = []

deny_messages = ["Non", "No", "NoN", "nOn", "deny", "DENY!", "Denied", "NON!"]

async def send_deny(update: Update):
    index = random.randint(0,len(deny_messages)-1)
    if update.message.reply_to_message != None:
        await update.message.reply_to_message.reply_text(deny_messages[index])
    else:
        await update.message.reply_text(deny_messages[index])
    
async def add_denied_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    denied_user.append(update.message.text.split(' ', 1)[1])

async def delete_denied_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    denied_user.remove(update.message.text.split(' ', 1)[1])

# HL des messages
async def handle_hl(update: Update, context: ContextTypes.DEFAULT_TYPE):   
    print("coucou")
    deny = False
    for user in denied_user:
        print("1")
        if user == update.message.from_user.username:
            deny = True
    print("1.5")
    if "@pam_deny_bot" in update.message.text:
        print("2")
        deny = True
    if deny:
        print("2.5")
        await send_deny(update)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(
        "remove", delete_denied_command))
    application.add_handler(CommandHandler(
        "add", add_denied_command))

    application.add_handler(MessageHandler(filters.ALL, handle_hl))
    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()