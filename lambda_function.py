import json
import os
from slack import WebClient
from slack.errors import SlackApiError
from piazza_api import Piazza

def lambda_handler(event, context):
    p = Piazza()
    p.user_login(os.environ['piazza_email'], os.environ['piazza_password'])

    client = WebClient(token=os.environ['slack_token'])
    try:
        response = client.chat_postMessage(
        channel='#random',
        text="Hello world!")
        assert response["message"]["text"] == "Hello world!"
    except SlackApiError as e:
        print(e)