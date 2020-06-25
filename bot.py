import os

import telegram.error
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

COMMANDS_TEXT = """
start - Initialize the bot and see startup instructions
send - `/send $chat_id $text_message` Send a message $text_message to a chat with id $chat_id where the bot is enabled
enable_subscriptions - `/enable_subscriptions` Enable the current chat for subscriptions from other users
subscribe - `/subscribe $chat_id` Receive notifications from a chat $chat_id where the bot is enabled
unsubscribe - `/unsubscribe $chat_id` Unsubscribe from chat $chat_id
"""

HELP_TEXT = """Hello there! To use this bot, you need to get the chat id of\
 the chat you want to send the message to. This will not be stored on the bot\
 for security reasons. You will have to use this chat id every time you send a\
 message. When you add this bot to a group or channel, and run /start command,\
 it will automatically grab the chat id and send it in the message. You can\
 save that somewhere (or maybe create an index of chat ids to the\
 groups/channels).
 To send a text message, use the /send command with the syntax\
 <code>/send $chat_id $text_message</code> and replace the chat_id with the\
 chat id of\
 receiving chat, and the text_message as the text you want to send."""

SUBSCRIPTIONS = dict()


def start(update, context):
    chat_id = str(update.effective_chat.id)
    if update.effective_chat.type in ["group", "channel", "supergroup"]:
        context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"The chat id of this chat is {chat_id}."
                " Save this somewhere (like your Saved Messages)"
            ),
        )
    else:
        context.bot.send_message(chat_id=chat_id, text=HELP_TEXT, parse_mode="HTML")


def send_message(update, context):
    text = update.message.text
    _, receiving_chat_id, content = text.split(" ", 2)

    context.bot.send_message(chat_id=receiving_chat_id, text=content, parse_mode="HTML")


def enable_for_subscriptions(update, context):
    chat_id = str(update.effective_chat.id)
    if not SUBSCRIPTIONS.get(chat_id):
        SUBSCRIPTIONS[chat_id] = set()
        message = (
            f"The chat id of this chat is {chat_id}."
            " Save this somewhere (like your Saved Messages)"
        )
    else:
        message = (
            "Chat is already enabled for subscriptions. " f"The chat id is {chat_id}"
        )

    context.bot.send_message(chat_id=chat_id, text=message)


def subscribe(update, context):
    text = update.message.text
    _, chat_id = text.split(" ", 1)

    if SUBSCRIPTIONS.get(chat_id) is not None:
        SUBSCRIPTIONS.get(chat_id).add(str(update.effective_chat.id))
        message = f"Subscribed to chat id {chat_id}"
    else:
        message = (
            f"No chat with id {chat_id} found."
            " Have you enabled the chat for subscriptions?"
        )

    context.bot.send_message(chat_id=str(update.effective_chat.id), text=message)


def unsubscribe(update, context):
    text = update.message.text
    _, chat_id = text.split(" ", 1)
    this_chat_id = str(update.effective_chat.id)

    if not SUBSCRIPTIONS.get(chat_id) or not this_chat_id in SUBSCRIPTIONS[chat_id]:
        message = f"You aren't subscribed to chat {chat_id}"
    else:
        SUBSCRIPTIONS[chat_id].remove(this_chat_id)
        message = f"Unsubscribed from chat {chat_id}"

    context.bot.send_message(chat_id=this_chat_id, text=message)


def receive_message(update, context):
    message = f"<code>{update.effective_chat.title or 'private'}:</code> {update.message.text}"
    kwargs = {'parse_mode': "HTML"}
    for receiver_id in SUBSCRIPTIONS.get(str(update.effective_chat.id), []):
        try:
            context.bot.send_message(chat_id=receiver_id, text=message, **kwargs)
        except telegram.error.BadRequest:
            message = f"From: {update.effective_chat.title or 'private'}\n{update.message.text}"
            kwargs = {}
            context.bot.send_message(chat_id=receiver_id, text=message)


start_handler = CommandHandler("start", start)
send_text_handler = CommandHandler("send", send_message)
subscribe_handler = CommandHandler("subscribe", subscribe)
unsubscribe_handler = CommandHandler("unsubscribe", unsubscribe)
enable_subscription_handler = CommandHandler(
    "enable_subscriptions", enable_for_subscriptions
)
message_handler = MessageHandler(Filters.text & (~Filters.command), receive_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(send_text_handler)
dispatcher.add_handler(enable_subscription_handler)
dispatcher.add_handler(subscribe_handler)
dispatcher.add_handler(unsubscribe_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
