# Stock News Alert

A Python script that tracks stock price changes and sends news alerts via email.  
Whenever a stock price changes by 5% or more between consecutive days, the script fetches the latest news about the company and notifies you.

---

## Features

- Tracks daily stock price changes using Alpha Vantage API.
- Fetches relevant news articles using NewsAPI.
- Sends email notifications when significant stock movements occur.
- Highlights whether the stock went up (🔺) or down (🔻).

---

## Prerequisites

- Python 3.10 or higher
- Libraries:
  - `requests`
  - `python-dotenv`

---

## Setup Instructions

**Clone the repository:**

```bash
git clone https://github.com/Obasi090/stock-news-alert.git
cd stock-news-alert
```

**Install required packages:**
```bash
pip install -r requirements.txt
```
**Create a .env file in the project root with your API keys and email credentials:**
```env
ALPHA_API_KEY=your_alpha_vantage_api_key
NEWS_API_KEY=your_newsapi_key
EMAIL_ADDRESS=your_email@example.com
my_email_password=your_email_password
RECIPIENT_ADDRESS=recipient_email@example.com
```
**Usage:**
```bash
python main.py
```

**Customization**
- Change the stock symbol by updating the STOCK variable in main.py.
- Change the company name for news alerts by updating the COMPANY_NAME variable.
- To add more recipients, modify the RECIPIENT_ADDRESS in .env.

**Optional Improvements**
- Add SMS notifications using Twilio API (currently not included due to regional restrictions).
- Use logging to track script execution and errors.
- Schedule the script with cron (Linux/macOS) or Task Scheduler (Windows) for automated daily checks.
