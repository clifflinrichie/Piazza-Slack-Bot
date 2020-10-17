import json
from slack import WebClient
from slack.errors import SlackApiError
from piazza_api import Piazza
from piazza_function import get_post_attr, pretty_print
import os

def lambda_handler(event, context):
    p = Piazza()
    p.user_login(os.environ['piazza_email'],os.environ['piazza_password'])
    user_profile = p.get_user_profile()
    myEvent = event['event']
    client = WebClient(token=os.environ['slack_token'])


    if(myEvent['type'] == 'app_mention'):
        if(('Show me the last' in myEvent['text']) and ('piazza post(s)' in myEvent['text'])):
            question = myEvent['text']
            num_recent = (question.replace('Show me the last ', '').replace(' piazza post(s)', '')).split(' ', 2)[1]
            my_class = p.network(os.environ["CS2110"])
            posts = my_class.iter_all_posts(limit=int(num_recent))
            all_post_attr = get_post_attr(posts)
            my_text = ""
            for post in all_post_attr:
                my_text += pretty_print(post)

            response = client.chat_postMessage(
                channel=event['channel'],
                text=my_text)