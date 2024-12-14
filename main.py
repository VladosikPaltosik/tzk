import logging
import os
import time

from dotenv import load_dotenv
import psutil
import thingspeak

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_metrics.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables from a .env file
load_dotenv()

# Constants for Thingspeak configuration
CHANNEL_ID = os.getenv('CHANNEL_ID')
WRITE_API_KEY = os.getenv('WRITE_API_KEY')

channel = thingspeak.Channel(id=CHANNEL_ID, api_key=WRITE_API_KEY)


def update_channels():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    try:
        # Send data to ThingSpeak
        response = channel.update({1: cpu_usage, 2: memory_usage})

        # Log data and response
        logging.info(f"CPU Usage (%): {cpu_usage}")
        logging.info(f"Memory Usage (%): {memory_usage}")
        logging.info(f"ThingSpeak Response: {response}")
    except Exception as ex:
        logging.error(f"Connection failed: {ex}")


def main():
    if not CHANNEL_ID or not WRITE_API_KEY:
        raise ValueError("CHANNEL_ID and WRITE_API_KEY must be set in the environment variables.")

    while True:
        update_channels()
        time.sleep(16)


if __name__ == "__main__":
    main()
