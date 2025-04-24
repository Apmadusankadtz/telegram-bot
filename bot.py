from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import instaloader
import requests

# Bot Token
TOKEN = '7722888756:AAFWjAt7mEe14Dunr6VlGUAvOOJD4weuoJ0'

# Download Instagram image URL using instaloader
def get_instagram_image_url(url):
    loader = instaloader.Instaloader(download_pictures=True, save_metadata=False, post_metadata_txt_pattern="")
    shortcode = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    return post.url  # Original image URL

# Telegram bot handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send photo link")

def handle_message(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    try:
        img_url = get_instagram_image_url(url)

        # Download the image temporarily
        response = requests.get(img_url)
        with open("temp.jpg", "wb") as f:
            f.write(response.content)

        # Send the actual image file
        with open("temp.jpg", "rb") as img:
            update.message.reply_photo(photo=img)

        # Delete after sending
        import os
        os.remove("temp.jpg")

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
