import csv
import logging
import os
import asyncio
import random
import sys
from colorama import Fore, Style, init
from telethon import TelegramClient
from telethon.errors import PeerIdInvalidError, UserIdInvalidError, FloodWaitError
from datetime import datetime
import json

# Initialize colorama for colored terminal output
init(autoreset=True)

# Load profiles from JSON file
with open('telegram_profiles.json', 'r') as file:
    profiles_data = json.load(file)
    PROFILES = profiles_data["PROFILES"]

CSV_FILE_PATH = 'telegramy.csv'
MESSAGES_FILE_PATH = 'messages.txt'  # Path to the external messages file

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='telegram_client.log'
)
logger = logging.getLogger(__name__)

def load_welcome_messages(file_path):
    """Load welcome messages from an external file."""
    if not os.path.exists(file_path):
        print(Fore.RED + f"Error: {file_path} not found.")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        messages = [line.strip() for line in f if line.strip()]
    return messages

def display_welcome():
    print(Fore.CYAN + Style.BRIGHT + "\n" + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "         📬 Welcome to the Advanced Message Sender 📬       ")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60 + Style.RESET_ALL)
    print(Fore.YELLOW + "              Optimized for smooth communication           ")
    print(Fore.CYAN + "=" * 60 + "\n" + Style.RESET_ALL)

class TelegramSender:
    def __init__(self, api_id, api_hash, phone_number, session_name, profile_name, profile_color):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.phone_number = phone_number
        self.profile_name = profile_name
        self.profile_color = profile_color
        self.sent_count = 0
        self.failures = 0
        self.restricted = False  # Tracks if the account is restricted

    async def start_client(self):
        try:
            await self.client.start()
            if not await self.client.is_user_authorized():
                print(self.profile_color + "🔐 Not authorized. Requesting code...")
                await self.client.send_code_request(self.phone_number)
                code = input(self.profile_color + 'Enter the code you received: ')
                await self.client.sign_in(self.phone_number, code)
        except Exception as e:
            logger.error(f"Error starting Telegram client: {e}")
            print(self.profile_color + f"⚠️ Failed to start client for {self.phone_number}. Error: {e}")

    async def get_user_entity(self, username):
        try:
            entity = await self.client.get_entity(username)
            return entity
        except (PeerIdInvalidError, UserIdInvalidError):
            logger.warning(self.profile_color + f"⚠️ Invalid username: {username}")
            return None
        except Exception as e:
            logger.error(self.profile_color + f"⚠️ Failed to get entity for {username}: {e}")
            return None

    async def conversation_exists(self, entity):
        try:
            messages = await self.client.get_messages(entity, limit=1)
            return len(messages) > 0
        except Exception as e:
            logger.error(f"⚠️ Error checking conversation with {entity.id}: {e}")
            return False

    async def send_welcome_message(self, username, messages):
        try:
            entity = await self.get_user_entity(username)
            if entity and not await self.conversation_exists(entity):
                message = random.choice(messages)
                await self.client.send_message(entity, message)
                self.sent_count += 1
                self.failures = 0  # Reset failures on success
                print(self.profile_color + f"✅ {self.profile_name} - Welcome message sent to {username}")
                return True
            else:
                print(Fore.YELLOW + f"⏩ {self.profile_name} - Conversation already exists with {username}. Skipping and removing from CSV...")
                return 'exists'
        except FloodWaitError as e:
            print(Fore.RED + f"⏳ {self.profile_name} - Rate limited. Waiting for {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
            self.failures += 1
            if self.failures >= 5:
                self.restricted = True
            return 'failed'
        except Exception as e:
            logger.error(self.profile_color + f"⚠️ Unexpected error sending message to {username}: {e}")
            self.failures += 1
            if self.failures >= 5:
                self.restricted = True
            return 'failed'

def load_users(csv_file_path):
    if not os.path.exists(csv_file_path):
        logger.error(Fore.RED + f"CSV file not found: {csv_file_path}. Creating a new one.")
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_file.write("")  # Create an empty file
        return []
    with open(csv_file_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        return [row[0].strip() for row in csv_reader if row and row[0].strip()]

def remove_user_from_csv(csv_file_path, user_to_remove):
    if not os.path.exists(csv_file_path):
        logger.error(Fore.RED + f"CSV file not found: {csv_file_path}")
        return

    with open(csv_file_path, 'r', newline='') as csv_file:
        rows = list(csv.reader(csv_file))

    updated_rows = [row for row in rows if row and row[0].strip() != user_to_remove]

    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(updated_rows)

    print(Fore.YELLOW + f"🗑️ User {user_to_remove} removed from CSV.")

async def main():
    display_welcome()
    start_time = datetime.now()

    # Load messages from an external file
    WELCOME_MESSAGES = load_welcome_messages(MESSAGES_FILE_PATH)
    if not WELCOME_MESSAGES:
        print(Fore.RED + "❌ No messages found in the file. Exiting.")
        return

    users = load_users(CSV_FILE_PATH)
    if not users:
        print(Fore.RED + "❌ No users to process.")
        return

    profile_senders = [
        TelegramSender(PROFILES[0]['API_ID'], PROFILES[0]['API_HASH'], PROFILES[0]['PHONE_NUMBER'],
                       PROFILES[0]['SESSION_NAME'], PROFILES[0]['NAME'], PROFILES[0]['COLOR']),
        TelegramSender(PROFILES[1]['API_ID'], PROFILES[1]['API_HASH'], PROFILES[1]['PHONE_NUMBER'],
                       PROFILES[1]['SESSION_NAME'], PROFILES[1]['NAME'], PROFILES[1]['COLOR'])
    ]

    for sender in profile_senders:
        await sender.start_client()

    index = 0
    while index < len(users):
        user = users[index]
        sent = False

        for sender in profile_senders:
            if sender.restricted:
                continue

            status = await sender.send_welcome_message(user, WELCOME_MESSAGES)

            if status == 'exists':
                remove_user_from_csv(CSV_FILE_PATH, user)
                index += 1
                sent = True
                break
            elif status == True:
                remove_user_from_csv(CSV_FILE_PATH, user)
                index += 1
                sent = True
                break

            # Check if all profiles are restricted
            if all(s.restricted for s in profile_senders):
                print(Fore.RED + "❌ Both profiles are restricted. Exiting.")
                duration = datetime.now() - start_time
                total_sent = sum(s.sent_count for s in profile_senders)
                print(Fore.GREEN + f"\nTotal messages sent: {total_sent}\nRuntime: {duration}\n")
                sys.exit(0)

            # Display message count
            print(
                Fore.CYAN + f"📊 Total messages sent so far:\n{profile_senders[0].profile_name}: {profile_senders[0].sent_count}\n{profile_senders[1].profile_name}: {profile_senders[1].sent_count}\n" + "=" * 50)

            await asyncio.sleep(random.uniform(1, 3))  # Balanced delay

    for sender in profile_senders:
        await sender.client.disconnect()
    duration = datetime.now() - start_time
    print(Fore.GREEN + Style.BRIGHT + f"\n🎉 Messaging process completed! \nTotal Runtime: {duration}\n" + "=" * 50)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Program interrupted. Exiting gracefully...")
        sys.exit(0)
