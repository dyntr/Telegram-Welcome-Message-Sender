# Telegram Advanced Message Sender

This script automates sending welcome messages to users from a CSV file via two Telegram profiles. It handles messaging limits, rate restrictions, and errors, ensuring smooth communication by balancing the load between profiles.

## Table of Contents
1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
3. [Configuration](#configuration)
4. [Functionality](#functionality)
5. [Classes and Functions](#classes-and-functions)
6. [Usage](#usage)
7. [Error Handling](#error-handling)
8. [Logging](#logging)
9. [FAQs and Troubleshooting](#faqs-and-troubleshooting)

---

## Overview
**Telegram Advanced Message Sender** automates the process of sending messages through two Telegram profiles, optimizing for rate limits and preventing duplicate messages to the same user. Each profile alternates sending messages and handles sending failures, restrictions, and other messaging errors.  

**Key Features:**
- **Multi-Profile Sending:** Balances message load across two profiles.
- **Error and Limit Management:** Handles errors like rate limits and logs detailed information for troubleshooting.
- **Real-Time Feedback:** Color-coded terminal output for an intuitive user experience.
- **CSV and Text File Integration:** Reads users from a CSV file and messages from a separate text file for modularity.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or later
- `telethon` library for Telegram client communication
- `colorama` library for colorful terminal output

### Installation
To install the required dependencies:
```bash
pip install telethon colorama
```

### Setup
1. **API Credentials**: Ensure you have API IDs, API hashes, and phone numbers for both Telegram profiles.
2. **CSV File**: Prepare a CSV file (`telegramy.csv`) containing usernames to whom you want to send messages.
3. **Message File**: Create a text file (`messages.txt`) with one message per line. These will be randomly selected when sending.

---

## Configuration

In the script, configure both Telegram profiles in the `PROFILES` variable:
```python
PROFILES = [
    {
        'API_ID': 'YOUR_API_ID_1',
        'API_HASH': 'YOUR_API_HASH_1',
        'PHONE_NUMBER': 'YOUR_PHONE_NUMBER_1',
        'SESSION_NAME': 'session_profile_1',
        'COLOR': Fore.LIGHTBLUE_EX,
        'NAME': 'Profile 1'
    },
    {
        'API_ID': 'YOUR_API_ID_2',
        'API_HASH': 'YOUR_API_HASH_2',
        'PHONE_NUMBER': 'YOUR_PHONE_NUMBER_2',
        'SESSION_NAME': 'session_profile_2',
        'COLOR': Fore.LIGHTRED_EX,
        'NAME': 'Profile 2'
    }
]
```

Update paths if your CSV or messages file is stored elsewhere:
```python
CSV_FILE_PATH = 'path/to/telegramy.csv'
MESSAGES_FILE_PATH = 'path/to/messages.txt'
```

---

## Functionality

1. **User Authentication**: Each profile authenticates with Telegram via an API ID, hash, and phone number.
2. **Load Messages and Users**: Messages are loaded from `messages.txt` and usernames from `telegramy.csv`.
3. **Sending Process**: 
   - Each profile tries to send messages, skipping users with existing conversations.
   - If restricted by rate limits, the script waits and retries.
4. **Removal from CSV**: Users are removed from the CSV after a successful message or if a conversation exists.
5. **Real-Time Status**: Displays sent message count, restrictions, and real-time status updates.

---

## Classes and Functions

### `display_welcome()`
Displays a welcome message in a colorful format to the terminal to provide a clear start to the session.

### `load_welcome_messages(file_path)`
Loads welcome messages from `messages.txt`. If the file does not exist or is empty, the function exits.

### `load_users(csv_file_path)`
Reads usernames from `telegramy.csv`. If the file is not found, it creates an empty one.

### `remove_user_from_csv(csv_file_path, user_to_remove)`
Removes a user from `telegramy.csv` after a successful message is sent or if a conversation exists.

### Class: `TelegramSender`

The `TelegramSender` class manages all Telegram-related actions for each profile. 

#### Methods:
- **`__init__(...)`**: Initializes API credentials, error counters, and status tracking.
- **`start_client()`**: Authenticates the client with Telegram. Prompts for a verification code if the user is unauthorized.
- **`get_user_entity(username)`**: Retrieves the Telegram entity for a username. Returns `None` if the username is invalid.
- **`conversation_exists(entity)`**: Checks if a conversation already exists with a user.
- **`send_welcome_message(username, messages)`**: Sends a welcome message if no prior conversation exists. Updates counters and handles errors like rate limits and failed messages.

---

## Usage

### Running the Script
To run the script:
```bash
python script_name.py
```

Upon starting, it:
- Loads all users and messages.
- Alternates message sending between profiles.
- Displays real-time status and error handling in the terminal.

### Stopping the Script
Press `Ctrl+C` to exit gracefully, which provides a summary of sent messages and runtime.

---

## Error Handling

The script handles various errors:
- **FloodWaitError**: Waits for the required time when a rate limit is hit and retries.
- **PeerIdInvalidError**: Logs and skips usernames that are invalid or restricted.
- **File Handling Errors**: Checks for missing or empty CSV and message files.

---

## Logging

Logs are recorded in `telegram_client.log`, capturing:
- Profile authentication steps
- Message sending status
- Errors and rate limit information

---

## FAQs and Troubleshooting

### Why are no messages being sent?
1. Check that `telegramy.csv` contains usernames.
2. Verify `messages.txt` is not empty.
3. Ensure API credentials are correct.

### How can I increase the delay between messages?
Modify the delay in the main loop:
```python
await asyncio.sleep(random.uniform(1, 3))  # Change 1-3 seconds as needed
```

### Why is a profile restricted?
Profiles may hit rate limits if too many messages are sent within a short period. If this happens, the script will wait before retrying.
