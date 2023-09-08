import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

registered_groups = []
channel_ids = [123456789, 987654321]  # Replace with your desired channel IDs

def start(update, context):
    # Create buttons for registered group chat IDs
    buttons = [InlineKeyboardButton(f"Group {group_id}", callback_data=f"group_{group_id}") for group_id in registered_groups]
    keyboard = [buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with buttons to the user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please select a group chat ID:",
                             reply_markup=reply_markup)
    

def button_callback(update, context):
    query = update.callback_query
    group_id = query.data

    # Forward the channel post to the selected group chat ID
    context.bot.forward_message(chat_id=group_id,
                                from_chat_id=query.message.chat.id,
                                message_id=query.message.message_id)

    # Send a confirmation message to the user
    context.bot.send_message(chat_id=query.message.chat.id,
                             text=f"Channel post forwarded to group {group_id}")

def register_group(update, context):
        # Open the file in append mode
    file_path = 'file.txt'  # Replace with the actual file path
    file = open(file_path, 'a')

    # Write content to the file
    content = str(update)
    file.write(content)

    # Close the file
    file.close()
    chat_id = update.message.chat_id

    if chat_id not in registered_groups:
        registered_groups.append( - chat_id)
        context.bot.send_message(chat_id=chat_id, text="Group chat ID registered successfully!")
    else:
        context.bot.send_message(chat_id=chat_id, text="Group chat ID is already registered.")

def forward_message_to_groups(update, context):
    logging.basicConfig(format='%(channel_ids)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    
    for group_id in registered_groups:        
        context.bot.send_message(chat_id=-group_id,
                                        text=str(update.channel_post.text))

    # # Check if the update has a message and the message is from a registered channel
    # if update.message and update.channel_post.chat_id in channel_ids:
    #     # Forward the message to all registered group chat IDs

def error_handler_callback(update, context):
    logger.error(msg="Exception occurred", exc_info=context.error)

def main():
    updater = Updater(token='5768711756:AAHkLBhDkAA69Ij6epnLQBvs-0PzP0b7iZE', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    button_callback_handler = CallbackQueryHandler(button_callback)
    dispatcher.add_handler(button_callback_handler)

    register_group_handler = CommandHandler('register', register_group)
    dispatcher.add_handler(register_group_handler)

    forward_message_handler = MessageHandler(Filters.chat_type.channel, forward_message_to_groups)
    dispatcher.add_handler(forward_message_handler)

    error_handler = MessageHandler(Filters.all, error_handler_callback)
    dispatcher.add_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
