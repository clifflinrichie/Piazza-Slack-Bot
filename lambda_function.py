import json
from slack import WebClient
from slack.errors import SlackApiError
from piazza_api import Piazza
import os

def lambda_handler(event, context):
    p = Piazza()
    p.user_login(os.environ['piazza_email'],os.environ['piazza_password'])
    user_profile = p.get_user_profile()
    print(event)
    myEvent = event['event']
    client = WebClient(token=os.environ['slack_token'])
    if(myEvent['type'] == 'app_mention'):
        if('Show me the posts for: ' in myEvent['text']):
            classId = myEvent['text']
            class_map = classId.split('Show me the posts for: ', 1)[1]

            my_class = p.network(os.environ[class_map])
            post = my_class.iter_all_posts(limit=1)
            date_created = ""
            subject = ""
            for x in post:
                history = x['history']
                main_post = history[0]
                date_created = x['created']
                subject = main_post['subject']
            print(subject[0])
            response = client.chat_postMessage(
                channel='#random',
                text="The most recent post: "+ subject +" was created on "+ date_created)