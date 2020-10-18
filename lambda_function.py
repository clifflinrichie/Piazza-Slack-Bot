import json
from slack import WebClient
from slack.errors import SlackApiError
from piazza_api import Piazza
import piazza_api
import re
from piazza_function import get_post_attr, pretty_print, pretty_print_instr
import os

def instructor_posts(my_class, instr_goal):
    max_cid = my_class.get_statistics()['total']['questions'] - 1
    cid = max_cid
    instr_goal = min(instr_goal, 10)
    num_instr = 0
    text = ""
    while(num_instr < instr_goal and cid > (max_cid - 25)):
        try:
            post = my_class.get_post(cid)
            all_post_attr = get_post_attr([post])
            post_text = pretty_print_instr(all_post_attr[0])
            if post_text != "":
                text+=post_text
                num_instr+=1
        except piazza_api.exceptions.RequestError:
            print(cid)
            pass
        cid-=1
    return text

def lambda_handler(event, context):
    p = Piazza()
    p.user_login(os.environ['piazza_email'], os.environ['piazza_password'])
    user_profile = p.get_user_profile()
    myEvent = event['event']
    client = WebClient(token=os.environ['slack_token'])


    if(myEvent['type'] == 'app_mention'):
        if(('Show me the last' in myEvent['text']) and ('piazza post(s)' in myEvent['text'])):
            question = myEvent['text']
            num_recent = (question.replace('Show me the last ', '').replace(' piazza post(s)', '')).strip().split(' ', 2)[1]
            my_class = p.network(os.environ["CS2110"])
            posts = my_class.iter_all_posts(limit=int(num_recent))
            all_post_attr = get_post_attr(posts)
            my_text = ""
            for post in all_post_attr:
                my_text += pretty_print(post)

            response = client.chat_postMessage(
                channel=myEvent['channel'],
                text=my_text)
        elif(('Show me the last' in myEvent['text']) and ('instructor post(s)' in myEvent['text'])):
            print(f"Event: {event}")
            print(f"**************")
            num_recent = re.search(r"(\s(\d+)\s)", myEvent['text'])[0].strip()
            print(myEvent['text'])
            print("Where is this? Recent:", num_recent, ":after")
            my_class = p.network(os.environ['CS2110'])
            my_text = instructor_posts(my_class, int(num_recent))
            response = client.chat_postMessage(
                channel=myEvent['channel'],
                text=my_text)
            