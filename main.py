import requests
import os
from dotenv import load_dotenv
load_dotenv()

import smtplib
from email.message import EmailMessage

import logging
logging.basicConfig(
    filename="stock.log",
    level= logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s"
)

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

def get_stock_data(stock_symbol):
    url = (
        "https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={stock_symbol}"
        f"&apikey={os.environ['ALPHA_API_KEY']}"
    )
    response = requests.get(url)
    data = response.json()
    return data["Time Series (Daily)"]

def calculate_change(daily_time):
    dates = list(daily_time.keys())
    yesterday = dates[0]
    day_before = dates[1]

    yesterday_close = float(daily_time[yesterday]["4. close"])
    day_before_close = float(daily_time[day_before]["4. close"])

    difference = yesterday_close - day_before_close
    percentage = round((difference / day_before_close) * 100, 2)

    direction = "🔺" if percentage > 0 else "🔻"

    return percentage, direction, day_before, yesterday


def fetch_news(company_name, start_date, end_date):
    url = (
        "https://newsapi.org/v2/everything"
        f"?q={company_name}&from={start_date}&to={end_date}"
        f"&sortBy=relevancy&apiKey={os.environ['NEWS_API_KEY']}"
    )
    response = requests.get(url)
    data = response.json()
    return data["articles"]


def send_email_alerts(stock, percentage, direction, articles):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(
            os.environ["EMAIL_ADDRESS"],
            os.environ["my_email_password"]
        )

        for article in articles[:3]:
            msg = EmailMessage()
            msg["Subject"] = f"{stock}: {direction}{abs(percentage)}%"
            msg["From"] = os.environ["EMAIL_ADDRESS"]
            msg["To"] = os.environ["RECIPIENT_ADDRESS"]
            msg.set_content(
                f"Headline: {article['title']}\n\n"
                f"Brief: {article['description']}"
            )
            smtp.send_message(msg)


def main():
    logging.info("Script started")

    daily_time = get_stock_data(STOCK)
    if not daily_time:
        return

    result = calculate_change(daily_time)
    if not result:
        return

    percentage, direction, start, end = result

    if abs(percentage) >= 5:
        logging.info("Threshold met. Fetching news.")
        articles = fetch_news(COMPANY_NAME, start, end)
        send_email_alerts(STOCK, percentage, direction, articles)
    else:
        logging.info("Stock movement less than 5%. No email sent.")


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

