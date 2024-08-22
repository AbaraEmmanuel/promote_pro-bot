import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Directly define your token here
TOKEN = "7432968296:AAEkaEPZ7Rlu0LHfIHc_hFnC12UIiaI2CSI"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define the mini app URL
MINI_APP_URL = "https://exquisitev2.urbanson.tech/"

# Store user data in memory (or use a database in a real application)
user_data = {}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    user_data[user_id] = {
        'username': username,
        'points': 0,
        'tasks_done': []
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

# Handle details for each service option and "Go Back" functionality
async def service_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

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
        keyboard = [
            [InlineKeyboardButton("MEXC", callback_data='token_mexc')],
            [InlineKeyboardButton("LBANK", callback_data='token_lbank')],
            [InlineKeyboardButton("BITFOREX", callback_data='token_bitforex')],
            [InlineKeyboardButton("BYBIT", callback_data='token_bybit')],
            [InlineKeyboardButton("GATE.IO", callback_data='token_gateio')],
            [InlineKeyboardButton("XT.COM", callback_data='token_xtcom')],
            [InlineKeyboardButton("CRYPTO.COM", callback_data='token_cryptocom')],
            [InlineKeyboardButton("BITGET", callback_data='token_bitget')],
            [InlineKeyboardButton("BITFINEX", callback_data='token_bitfinex')],
            [InlineKeyboardButton("BITRUE", callback_data='token_bitrue')],
            [InlineKeyboardButton("Go Back", callback_data='services')]
        ]
        await query.edit_message_text('SELECT A LISTING PLATFORM:', reply_markup=InlineKeyboardMarkup(keyboard))
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
        # Update the message instead of replying to avoid the 'NoneType' issue
        await query.message.edit_text('WELCOME! PLEASE CHOOSE AN OPTION:', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Services", callback_data='services')],
            [InlineKeyboardButton("Join Us", callback_data='join_us')],
            [InlineKeyboardButton("Events", callback_data='events')]
        ]))
    elif data == 'go_back_to_services':
        await handle_services(update, context)
    else:
        message = "INVALID OPTION SELECTED."
        keyboard = [
            [InlineKeyboardButton("Go Back", callback_data='services')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=message, reply_markup=reply_markup)

# Show Join Us options
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

# Main function
def main():
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_services, pattern='^services$'))
    application.add_handler(CallbackQueryHandler(service_details, pattern='^(promotion|token_listing|community_management|go_back_to_start|go_back_to_services)$'))
    application.add_handler(CallbackQueryHandler(handle_join_us, pattern='^join_us$'))

    application.run_polling()

if __name__ == '__main__':
    main()
