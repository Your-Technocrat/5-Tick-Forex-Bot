import os
import asyncio
import requests
import schedule
import time
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your Bot API token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Replace with your Telegram channel's username
CHANNEL_ID = "@Five_Tick_Forex"

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

# Function to send a message to the Telegram channel
async def send_message_to_channel(text):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
        print(f"Sent message: {text}")  # Confirm message sent
    except Exception as e:
        print(f"Failed to send message: {e}")

# Function to fetch a single news article from Alpha Vantage API
async def fetch_single_trading_news():
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={ALPHA_VANTAGE_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            # Check if there's news and send only the first one
            if news_data.get("feed"):
                first_news = news_data["feed"][0]  # Get the first news article
                title = first_news.get("title")
                link = first_news.get("url")
                await send_message_to_channel(f"{title}\n{link}")
            else:
                print("No news available.")
        else:
            print(f"Error fetching news: {response.status_code}")
    except Exception as e:
        print(f"Failed to fetch news: {e}")

# Schedule the news fetching function to run every 5 minutes
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

def schedule_news():
    # Schedule the news fetching every 5 minutes (instead of 30)
    schedule.every(5).minutes.do(lambda: asyncio.create_task(fetch_single_trading_news()))

if __name__ == "__main__":
    # Start scheduling news fetching
    print("Starting news scheduler...")
    schedule_news()

    # Start the event loop
    asyncio.run(run_schedule())
