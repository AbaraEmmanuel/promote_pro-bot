import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Directly define your token here
TOKEN = "7432968296:AAEkaEPZ7Rlu0LHfIHc_hFnC12UIiaI2CSI"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Store user data and active chats
user_data = {}
active_chats = {}

# Admin IDs (replace with actual admin Telegram IDs)
ADMIN_IDS = [7461926970, 6480285775]  # Add more admin IDs as needed

# Example events
events = [
    {"name": "Crypto Conference 2024", "date": "2024-10-01", "time": "10:00 AM", "ticket_url": "http://example.com/ticket1"},
    {"name": "Blockchain Workshop", "date": "2024-10-10", "time": "02:00 PM", "ticket_url": "http://example.com/ticket2"},
    {"name": "DeFi Summit", "date": "2024-10-20", "time": "11:00 AM", "ticket_url": "http://example.com/ticket3"},
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    user_data[user_id] = {
        'username': username,
    }

    keyboard = [
        [InlineKeyboardButton("Services", callback_data='services')],
        [InlineKeyboardButton("Join Us", callback_data='join_us')],
        [InlineKeyboardButton("Events", callback_data='events')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('WELCOME! PLEASE CHOOSE AN OPTION:', reply_markup=reply_markup)

# Show services options
async def handle_services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Promotion", callback_data='promotion')],
        [InlineKeyboardButton("Token Listing", callback_data='token_listing')],
        [InlineKeyboardButton("Community Management", callback_data='community_management')],
        [InlineKeyboardButton("Go Back", callback_data='go_back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('SELECT A SERVICE:', reply_markup=reply_markup)

# Handle Join Us selection
async def handle_join_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Shill Master", callback_data='shill_master')],
        [InlineKeyboardButton("Moderator", callback_data='moderator')],
        [InlineKeyboardButton("Social Media Manager", callback_data='social_media_manager')],
        [InlineKeyboardButton("Go Back", callback_data='go_back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('SELECT A ROLE YOU ARE INTERESTED IN:', reply_markup=reply_markup)


# Handle token listing selection and start live chat
async def service_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    username = query.from_user.username

    if data == 'promotion':
        keyboard = [
            [InlineKeyboardButton("X Shilling", callback_data='x_shilling')],
            [InlineKeyboardButton("Telegram Shilling", callback_data='telegram_shilling')],
            [InlineKeyboardButton("Telegram Members", callback_data='telegram_members')],
            [InlineKeyboardButton("YouTube Promotion", callback_data='youtube_promotion')],
            [InlineKeyboardButton("Instagram Followers", callback_data='instagram_followers')],
            [InlineKeyboardButton("LinkedIn Followers", callback_data='linkedin_followers')],
            [InlineKeyboardButton("X Followers", callback_data='x_followers')],
            [InlineKeyboardButton("X Likes", callback_data='x_likes')],
            [InlineKeyboardButton("X Repost", callback_data='x_repost')],
            [InlineKeyboardButton("Reel Views", callback_data='reel_views')],
            [InlineKeyboardButton("YouTube Views", callback_data='youtube_views')],
            [InlineKeyboardButton("TikTok Views", callback_data='tiktok_views')],
            [InlineKeyboardButton("TikTok Likes", callback_data='tiktok_likes')],
            [InlineKeyboardButton("Instagram Likes", callback_data='instagram_likes')],
            [InlineKeyboardButton("LinkedIn Likes", callback_data='linkedin_likes')],
            [InlineKeyboardButton("YouTube Likes", callback_data='youtube_likes')],
            [InlineKeyboardButton("Go Back", callback_data='services')]
        ]
        await query.edit_message_text('SELECT A PROMOTION SERVICE:', reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == 'token_listing':
        # Handle Token Listing
        keyboard = [
            [InlineKeyboardButton("MEXC", callback_data='token_mexc')],
            [InlineKeyboardButton("LBANK", callback_data='token_lbank')],
            [InlineKeyboardButton("BITFOREX", callback_data='token_bitforex')],
            [InlineKeyboardButton("BYBIT", callback_data='token_bybit')],
            [InlineKeyboardButton("GATE.IO", callback_data='token_gateio')],
            [InlineKeyboardButton("XT.COM", callback_data='token_xtcom')],
            [InlineKeyboardButton("CRYPTO.COM", callback_data='token_cryptocom')],
            [InlineKeyboardButton("BITGET", callback_data='token_bitget')],
            [InlineKeyboardButton("Go Back", callback_data='services')]
        ]
        await query.edit_message_text('SELECT A LISTING PLATFORM:', reply_markup=InlineKeyboardMarkup(keyboard))
    elif data.startswith('token_'):
        token_name = data.replace('token_', '').upper()
        await query.edit_message_text(f'You clicked on {token_name} token listing. An admin will contact you soon.')

        # Notify all admins of the user and token
        for admin_id in ADMIN_IDS:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"User {username} (ID: {user_id}) clicked on {token_name} token listing. Use /reply {user_id} <message> to respond."
            )

        # Start the chat session
        active_chats[user_id] = {
            'username': username,
            'admins': ADMIN_IDS,
            'assigned_admin': None,  # No admin is assigned initially
            'active': True
        }
        await context.bot.send_message(chat_id=user_id, text="")
    elif data == 'community_management':
        keyboard = [
            [InlineKeyboardButton("Community Manager", callback_data='community_manager')],
            [InlineKeyboardButton("24/7 Chat Moderation", callback_data='chat_moderation')],
            [InlineKeyboardButton("ChatBot Expert", callback_data='chatbot_expert')],
            [InlineKeyboardButton("Content Creator", callback_data='content_creator')],
            [InlineKeyboardButton("Social Media Manager", callback_data='social_media_manager')],
            [InlineKeyboardButton("Go Back", callback_data='services')]
        ]
        await query.edit_message_text('SELECT A ROLE UNDER COMMUNITY MANAGEMENT:', reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == 'go_back_to_start':
        await query.message.edit_text('WELCOME! PLEASE CHOOSE AN OPTION:', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Services", callback_data='services')],
            [InlineKeyboardButton("Join Us", callback_data='join_us')],
            [InlineKeyboardButton("Events", callback_data='events')]
        ]))

# Handle messages sent by users
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if user_id in active_chats and active_chats[user_id]['active']:
        assigned_admin = active_chats[user_id]['assigned_admin']

        if assigned_admin is not None:
            message = update.message.text
            await context.bot.send_message(
                chat_id=assigned_admin,
                text=f"Message from {user_data[user_id]['username']} (ID: {user_id}): {message}"
            )
        else:
            await update.message.reply_text("Your chat hasn't been assigned to an admin yet.")
    else:
        await update.message.reply_text("You are not in a live chat with an admin.")

# Admin replies to user using /reply <user_id> <message>
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = context.args
        user_id = int(args[0])
        message = " ".join(args[1:])
        admin_id = update.message.from_user.id
        admin_username = update.message.from_user.username  # Get admin username

        if user_id in active_chats and active_chats[user_id]['active']:
            assigned_admin = active_chats[user_id]['assigned_admin']

            # If no admin is assigned, lock the chat to this admin
            if assigned_admin is None:
                active_chats[user_id]['assigned_admin'] = admin_id
                await update.message.reply_text(f"You are now handling chat with {user_data[user_id]['username']} (ID: {user_id}).")
                
                # Notify other admins that the chat is now locked to this admin
                for other_admin_id in active_chats[user_id]['admins']:
                    if other_admin_id != admin_id:
                        await context.bot.send_message(
                            chat_id=other_admin_id,
                            text=f"Admin {admin_username} (ID: {admin_id}) is now handling the chat with {user_data[user_id]['username']} (ID: {user_id})."
                        )

            # Allow only the assigned admin to reply
            if active_chats[user_id]['assigned_admin'] == admin_id:
                await context.bot.send_message(chat_id=user_id, text=f"Admin: {message}")
            else:
                await update.message.reply_text(f"Sorry, this chat is assigned to another admin.")
        else:
            await update.message.reply_text("The user is not in an active chat.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /reply <user_id> <message>")

# End the chat with /endchat <user_id>
async def end_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = int(context.args[0])
        admin_id = update.message.from_user.id
        admin_username = update.message.from_user.username

        if user_id in active_chats and active_chats[user_id]['active']:
            assigned_admin = active_chats[user_id]['assigned_admin']

            if assigned_admin == admin_id:
                active_chats[user_id]['active'] = False
                await update.message.reply_text(f"Chat with {user_data[user_id]['username']} (ID: {user_id}) has been ended.")

                await context.bot.send_message(chat_id=user_id, text="The chat has been closed by the admin. Thank you!")

                # Show the main menu to the user
                keyboard = [
                    [InlineKeyboardButton("Services", callback_data='services')],
                    [InlineKeyboardButton("Join Us", callback_data='join_us')],
                    [InlineKeyboardButton("Events", callback_data='events')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_message(chat_id=user_id, text='WELCOME! PLEASE CHOOSE AN OPTION:', reply_markup=reply_markup)

                # Notify other admins about chat closure
                for other_admin_id in active_chats[user_id]['admins']:
                    if other_admin_id != admin_id:
                        await context.bot.send_message(
                            chat_id=other_admin_id,
                            text=f"Admin {admin_username} (ID: {admin_id}) has closed the chat with {user_data[user_id]['username']} (ID: {user_id})."
                        )
            else:
                await update.message.reply_text("You cannot end this chat as it is assigned to another admin.")
        else:
            await update.message.reply_text("The user is not in an active chat.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /endchat <user_id>")

# Show upcoming events with individual buttons
async def show_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if events:
        # Create a button for each event
        keyboard = [[InlineKeyboardButton(event["name"], callback_data=f"event_{index}")] for index, event in enumerate(events)]
        
        # Add the "Go Back" button to return to the main menu
        keyboard.append([InlineKeyboardButton("Go Back", callback_data='go_back_to_start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Here are the upcoming events:", reply_markup=reply_markup)
    else:
        await query.edit_message_text("No upcoming events at the moment.")

# Handle individual event details and show "Buy Ticket" link
async def show_event_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Extract the event index from the callback data
    event_index = int(query.data.split("_")[1])
    selected_event = events[event_index]

    # Display the selected event details with a "Buy Ticket" button and a "Go Back to Events" button
    event_message = f"Event: {selected_event['name']}\nDate: {selected_event['date']}\nTime: {selected_event['time']}"
    keyboard = [[InlineKeyboardButton("Buy Ticket", url=selected_event['ticket_url'])],
                [InlineKeyboardButton("Go Back to Events", callback_data='events')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(event_message, reply_markup=reply_markup)

# Main function to set up the bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Callback query handlers for services, events, join_us, etc.
    application.add_handler(CallbackQueryHandler(handle_services, pattern='^services$'))
    application.add_handler(CallbackQueryHandler(service_details, pattern='^(promotion|token_listing|token_.*|community_management|go_back_to_start)$'))
    application.add_handler(CallbackQueryHandler(handle_join_us, pattern='^join_us$'))
    application.add_handler(CallbackQueryHandler(show_events, pattern='^events$'))
    application.add_handler(CallbackQueryHandler(show_event_details, pattern='^event_\\d+$'))

    # Message and chat handling
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    
    # Admin commands
    application.add_handler(CommandHandler("reply", reply_to_user))
    application.add_handler(CommandHandler("endchat", end_chat))

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()
