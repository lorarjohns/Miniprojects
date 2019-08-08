#!/usr/bin/python3
def get_info():
    import requests
    from bs4 import BeautifulSoup

    # import time
    from urllib import request
    import json

    # If we want more symbols later
    # base_url = 'http://google.com/finance?q=' # set the bitcoin monitoring url
    # symbols = ['XBT', 'BTC', 'NYXBT', '$BCOIN']

    url = "http://google.com/finance?q=BTC"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    price = soup.find_all(id="knowledge-currency__tgt-amount")[0].text
    bitcoin_message = "Hey <@UHP1B0TK4>, Bitcoin is up to ${price} today."
    post = {"text": f"{bitcoin_message}"}

    try:
        json_data = json.dumps(post)
        slack_request = request.Request(
            "https://hooks.slack.com/services/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",
            data=json_data.encode("ascii"),
            headers={"Content-Type": "application/json"},
        )
        slack_response = request.urlopen(slack_request)
    except Exception as except_message:
        print(f"Exception: {str(except_message)}")
        # This is whisky table's URL
        # Go here to get the other one: https://api.slack.com/apps/AL1RJGJ5U/incoming-webhooks

if __name__ == "__main__":
    get_info()
