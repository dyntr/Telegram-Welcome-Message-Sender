
# 📬 Telegram Welcome Message Sender Configuration Guide

Welcome to the setup guide for the **Advanced Telegram Message Sender**. This guide will walk you through the process of configuring and running the script to ensure smooth communication with your Telegram contacts.

---

## Table of Contents

1. [Installation](#installation)
2. [Project Structure](#project-structure)
3. [Configuration Files](#configuration-files)
   - [telegram_profiles.json](#telegram_profilesjson)
   - [messages.txt](#messagestxt)
   - [telegramy.csv](#telegramycsv)
4. [Running the Script](#running-the-script)
5. [Expected Output](#expected-output)
6. [Troubleshooting](#troubleshooting)

---

### 1. Installation

To get started, ensure you have **Python 3.7+** installed on your machine. Follow these steps to set up the required dependencies.

1. Clone or download the project files to your local machine.
2. Open a terminal in the project directory and install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Dependencies include:
    - `telethon`: For interacting with Telegram's API.
    - `colorama`: For colored terminal output.
    - `asyncio`, `random`, and `sys`: Standard Python libraries for asynchronous operations, randomness, and system exit handling.

---

### 2. Project Structure

Ensure your project directory contains the following essential files:

```plaintext
telegram_message_sender/
├── main.py                # Main script file
├── telegram_profiles.json # Profiles configuration file
├── messages.txt           # List of welcome messages
├── telegramy.csv          # Usernames to message
└── telegram_client.log    # Log file for errors and events
```

---

### 3. Configuration Files

#### telegram_profiles.json

This file holds the configuration for the Telegram profiles used in sending messages. Each profile includes its unique API ID, API Hash, and phone number.

**Example JSON Structure:**

```json
{
  "PROFILES": [
    {
      "API_ID": "123456",
      "API_HASH": "abc123def456",
      "PHONE_NUMBER": "+1234567890",
      "SESSION_NAME": "session1",
      "NAME": "Profile 1",
      "COLOR": "\u001b[32m"
    },
    {
      "API_ID": "654321",
      "API_HASH": "654def321abc",
      "PHONE_NUMBER": "+0987654321",
      "SESSION_NAME": "session2",
      "NAME": "Profile 2",
      "COLOR": "\u001b[34m"
    }
  ]
}
```

- **API_ID** and **API_HASH** are provided by Telegram (register at [Telegram API](https://my.telegram.org/)).
- **PHONE_NUMBER**: The number associated with each Telegram profile.
- **SESSION_NAME**: Unique name for the session file.
- **NAME**: Display name for the profile.
- **COLOR**: Color for each profile’s terminal output.

#### messages.txt

Contains the welcome messages to be sent. Place each message on a new line. The script will randomly select one for each user.

**Example:**

```plaintext
Welcome! We're excited to have you here.
Hi there! Looking forward to connecting.
Thanks for joining us! Let's keep in touch.
```

#### telegramy.csv

A CSV file listing the usernames of individuals to whom messages will be sent. Ensure each username is on a new line in the first column.

**Example:**

```plaintext
username1
username2
username3
```

---

### 4. Running the Script

Run the script using the following command:

```bash
python main.py
```

The script will display a welcome graphic and begin processing users from the CSV file, alternating between the profiles configured in `telegram_profiles.json`. Messages will be sent based on availability, balancing limits, and errors.

### 5. Expected Output

The script produces a colorful and informative terminal output with the following details:

- **Message Delivery Status**: Shows successful messages and existing conversations, with a count of messages sent per profile.
- **Errors and Rate Limits**: Displays any failures and rate limits encountered, pausing until restrictions lift.
- **Completion Summary**: Shows a final count of messages sent from each profile and the total runtime.

---

### 6. Troubleshooting

**Common Issues and Solutions:**

- **Rate Limit Exceeded**: If a profile is restricted, the script will switch to an alternate profile. Once both profiles are restricted, the process stops.
- **Invalid Username**: If a username is invalid, it’s logged as a warning and skipped.
- **No Users to Process**: Ensure `telegramy.csv` contains valid usernames.
- **Missing Files**: The script will halt if critical files (`telegram_profiles.json`, `messages.txt`, or `telegramy.csv`) are missing. Ensure all files are in the project directory.

For further issues, consult the `telegram_client.log` for detailed logs.

---

🎉 **Congratulations! You’re now ready to automate your Telegram messages.**
