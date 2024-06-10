# Telegram Total Assets Bot

This Telegram bot shows your total assets and their equivalent in a specified currency.

# Features
- Welcome message
- Command to display total assets and equivalent value in specified currency

# Requirements
- Python python 3.11.8 
- Telegram bot API token
- Gate.io SECRET & API key

# Step 1: *Create a Telegram Bot*
Open Telegram and search for @BotFather.
Start a chat and use the /start command.
Use the /newbot command and follow the instructions to create a new bot.
After creating the bot, you will receive a token. Save this token as you will need it later.

# Step 2: *Setup*
1. Clone the repository
2. Open cmd on the cloned project path 
3. Create virtuel env 'cmd' : python -m venv venv 
4. Activate the venv 'cmd' : .venv\Scripts\activate 
5. Install the requirement library 'cmd' : pip install -r requirements.txt 
6. Create a dont_share.py file with:
	# Replace with your actual Gate.io API credentials and Telegram bot token
		api_key = 'api_key'
		api_secret = 'api_secret'
		telegram_token = 'telegram_token'

# Step 2: *Run the script*
1. python gate_telegram_bot.py
2. go to your bot and start talking to it:
	# How the bot works:
		Start Command: When a user sends /start, the bot replies with a welcome message.
		Total Assets Command: When a user sends /totalassets <currency>, the bot fetches the total assets in USDT and their equivalent in the specified currency.
