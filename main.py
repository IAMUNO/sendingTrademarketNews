from twilio.rest import Client
import requests

STOCK_NAME = "IBM"  # STOCK_NAME you want to know
COMPANY_NAME = "IBM Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR OWN STOCK_API_KEY"
NEWS_API_KEY = "YOUR OWN NEWS_API_KEY"
TWILIO_SID = "YOUR OWN TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR OWN TWILIO_AUTH_TOKEN"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
print(data)

data_list = [value for (key, value) in data.items()]
print(data_list)

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 0:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    article = news_response.json()["articles"]
    print(article)
    two_articles = article[:2]
    print(two_articles)

    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\n\nHeadline: {article['title']}, \n\nBrief: {article['description']}"
        for article in two_articles
    ]

    print(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+Your twilio number",
            to="+Your phone number",
        )
