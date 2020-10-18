from slack import WebClient
from slack.errors import SlackApiError
from piazza_api import Piazza
import piazza_api
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
    client = WebClient(token=os.environ['slack_token'])

    myEvent = event['event']
    question = myEvent['text']

    if(myEvent['type'] == 'app_mention'):
        if (('answer' in myEvent['text']) and ('post' in myEvent['text'])):
            list_recent = [int(x) for x in question.split() if x.isdigit()]
            num_recent = list_recent[0]
            my_class = p.network(os.environ['CS2110'])
            my_text = instructor_posts(my_class, int(num_recent))
            response = client.chat_postMessage(
                channel=myEvent['channel'],
                text=my_text)
        elif(('instructor' not in myEvent['text']) and ('post' in myEvent['text'])):
            list_recent = [int(x) for x in question.split() if x.isdigit()]
            num_recent = list_recent[0]
            my_class = p.network(os.environ["CS2110"])
            posts = my_class.iter_all_posts(limit=int(num_recent))
            all_post_attr = get_post_attr(posts)
            my_text = ""
            for post in all_post_attr:
                my_text += pretty_print(post)

            response = client.chat_postMessage(
                channel=myEvent['channel'],
                text=my_text)