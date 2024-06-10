import hmac
import hashlib
import time
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import dont_share as ds
from gen_signature import gen_sign

# Define your API keys
API_KEY = ds.api_key
SECRET_KEY = ds.api_secret
TELEGRAM_TOKEN = ds.telegram_token

host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {"Accept": "application/json", "Content-Type": "application/json"}


def get_account_balances():

    url = "/wallet/total_balance"
    query_param = ""
    # for `gen_sign` implementation, refer to section `Authentication` in gate.io API
    sign_headers = gen_sign("GET", prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request("GET", host + prefix + url, headers=headers)
    json_object = r.json()
    balance = json_object["total"]["amount"]
    print(balance)
    return balance


def get_ticker(symbol):
    url = '/spot/tickers'
    query_param = f"currency_pair={symbol}"
    response = requests.request(
        "GET", host + prefix + url + "?" + query_param, headers=headers
    )
    # print(f"Ticker response: {response.text}")
    return response.json()


def get_total_assets_and_equivalent(target_currency="SOL"):
    # Get balances
    balance = get_account_balances()
    if balance:
        total_usdt = float(balance)
        # Get the conversion rate to the target currency
        ticker = get_ticker(target_currency + "_USDT")
        ticker = ticker[0] #get the first element in the resulted table
        if "last" not in ticker:
            return f"Error fetching ticker for {target_currency}"

        print(ticker["last"])
        conversion_rate = float(ticker["last"])
        equivalent_in_target_currency = total_usdt/conversion_rate

        # Prepare the result message
        result_message = (
            f"Total USDT equivalent: {total_usdt:.2f} USDT\n"
            f"Equivalent in {target_currency}: {equivalent_in_target_currency:.2f} {target_currency}"
        )
        return result_message
    else:
        return "Error fetching balance"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome! Use /totalassets <currency> to get your total assets and their equivalent in the specified currency."
    )


async def totalassets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    target_currency = " ".join(context.args).strip().upper()
    if not target_currency:
        await update.message.reply_text(
            "Please specify a target currency, e.g., /totalassets SOL"
        )
        return

    result_message = get_total_assets_and_equivalent(target_currency)
    await update.message.reply_text(result_message)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("totalassets", totalassets))

    app.run_polling()


if __name__ == "__main__":
    main()
