import json
from slack import WebClient
from slack.errors import SlackApiError


def lambda_handler(event, context):
    client = WebClient(token='xoxb-1434731635618-1431758020501-skg9O2Y9qVP9qsgrbEg5Xrga')
    try:
        response = client.chat_postMessage(
        channel='#random',
        text="Hello world!")
        assert response["message"]["text"] == "Hello world!"
    except SlackApiError as e:
        print(e)