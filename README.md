# Telegram Advanced Message Sender

This script automates sending welcome messages to users from a CSV file using two Telegram profiles. It is designed to handle messaging limits, rate restrictions, and errors, while balancing the load between profiles.

## Table of Contents
1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
3. [Configuration](#configuration)
4. [Script Structure and Functionality](#script-structure-and-functionality)
5. [Usage](#usage)
6. [Error Handling](#error-handling)
7. [Logging](#logging)
8. [FAQs and Troubleshooting](#faqs-and-troubleshooting)

---

## Overview
**Telegram Advanced Message Sender** automates sending messages through two Telegram profiles, optimizing for rate limits and preventing duplicate messages to the same user. Each profile alternates sending messages, handling sending failures, restrictions, and other messaging errors.

**Key Features:**
- **Multi-Profile Sending:** Balances message load across two profiles.
- **Error and Limit Management:** Handles errors like rate limits and logs detailed information for troubleshooting.
- **Real-Time Feedback:** Color-coded terminal output for intuitive feedback.
- **CSV and Text File Integration:** Reads users from a CSV file and messages from a text file for modularity.

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
1. **API Credentials**: Make sure to have API IDs, API hashes, and phone numbers for both Telegram profiles.
2. **CSV File**: Prepare a CSV file (`telegramy.csv`) containing usernames to whom you want to send messages.
3. **Message File**: Create a text file (`messages.txt`) with one message per line.

---

## Configuration

This script uses profiles loaded from a JSON file (`telegram_profiles.json`). Example JSON structure:

```json
{
    "PROFILES": [
        {
            "API_ID": "YOUR_API_ID_1",
            "API_HASH": "YOUR_API_HASH_1",
            "PHONE_NUMBER": "YOUR_PHONE_NUMBER_1",
            "SESSION_NAME": "session_profile_1",
            "COLOR": "LIGHTBLUE_EX",
            "NAME": "Profile 1"
        },
        {
            "API_ID": "YOUR_API_ID_2",
            "API_HASH": "YOUR_API_HASH_2",
            "PHONE_NUMBER": "YOUR_PHONE_NUMBER_2",
            "SESSION_NAME": "session_profile_2",
            "COLOR": "LIGHTRED_EX",
            "NAME": "Profile 2"
        }
    ]
}
```

Load the profiles in the script with:
```python
import json

# Load profiles from JSON file
with open('telegram_profiles.json', 'r') as file:
    profiles_data = json.load(file)
    PROFILES = profiles_data["PROFILES"]
```

---

## Script Structure and Functionality

1. **`display_welcome()`**
   Displays a welcome message with colored formatting to signal the start of the messaging process.

2. **`load_welcome_messages(file_path)`**
   Loads welcome messages from an external file. If the file doesn’t exist or is empty, an error message is displayed.

3. **`load_users(csv_file_path)`**
   Reads usernames from the CSV file. If the file is missing, it creates an empty one.

4. **`remove_user_from_csv(csv_file_path, user_to_remove)`**
   Removes a processed user from the CSV file, ensuring no duplicate messages are sent.

5. **Class: `TelegramSender`**
   Manages Telegram interactions for each profile. Responsible for connecting, sending messages, handling rate limits, and error tracking.

   - **Methods**:
      - **`__init__(...)`**: Initializes credentials and sets up error counters and tracking.
      - **`start_client()`**: Authenticates the client with Telegram, prompting for a verification code if unauthorized.
      - **`get_user_entity(username)`**: Retrieves the Telegram entity for a username.
      - **`conversation_exists(entity)`**: Checks if a conversation already exists with a user.
      - **`send_welcome_message(username, messages)`**: Sends a message if no prior conversation exists, updating counters and handling errors.

---

## Usage

### Running the Script
To start the script:
```bash
python script_name.py
```

The script:
- Loads all users and messages.
- Alternates message sending between profiles.
- Displays real-time status and error handling in the terminal.

### Stopping the Script
Press `Ctrl+C` to exit gracefully, providing a summary of sent messages and runtime.

---

## Error Handling

The script manages errors and provides feedback:
- **FloodWaitError**: Pauses for the required time when rate limits are hit.
- **PeerIdInvalidError/UserIdInvalidError**: Skips invalid or restricted usernames.
- **File Handling Errors**: Checks for missing or empty CSV and message files.

---

## Logging

Logs are recorded in `telegram_client.log`, capturing:
- Profile authentication steps
- Message sending status
- Errors and rate limit information

---

## FAQs and Troubleshooting

### Why aren’t messages being sent?
1. Verify `telegramy.csv` contains usernames.
2. Ensure `messages.txt` has messages.
3. Confirm API credentials are correct.

### How to adjust delay between messages?
Modify the delay in the main loop:
```python
await asyncio.sleep(random.uniform(1, 3))  # Adjust as needed
```

### What if a profile gets restricted?
Profiles may be rate-limited if too many messages are sent rapidly. The script will automatically retry after a wait period.
