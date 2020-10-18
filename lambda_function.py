import json
from slack import WebClient
from slack.errors import SlackApiError
from piazza_api import Piazza
from piazza_function import get_post_attr, pretty_print
import os

def lambda_handler(event, context):
    p = Piazza()
    p.user_login(os.environ['PIAZZA_EMAIL'],os.environ['PIAZZA_PASSWORD'])
    user_profile = p.get_user_profile()

    user_id = user_profile['user_id']
    print(event)
    myEvent = event['event']
    client = WebClient(token=os.environ['slack_token'])

    if(myEvent['type'] == 'message'):
        if ('Check if in class: ' in myEvent['text']):
            nameID = myEvent['text']
            name = nameID.split('Check if in class: ', 1)[1]
            print("name input: " + str(name))
            cs2110 = p.network(os.environ['class_map'])    # CS 2110 
            
            students = cs2110.get_users([user_id]) # returns dictionary of user(s) information
            # user not in class
            print(students)
            if (not students):
                response = client.chat_postMessage(
                channel=myEvent['channel'],
                text="User does not exist in this class")
            else:
                for student in students:
                    myName = student['name']
                    myID = student['id']
                    myRole = student['role']
                    response = client.chat_postMessage(
                    channel=myEvent['channel'],
                    text="The student " + myName + " is a " + myRole + " and has the ID " + myID)

    if(myEvent['type'] == 'app_mention'):
        if(('Show me the last' in myEvent['text']) and ('piazza post(s)' in myEvent['text'])):
            question = myEvent['text']
            my_class = p.network(os.environ["CS2110"])
            all_post_attr = []
            my_text = ""

            if (('by professor' in myEvent['text'])):
                question = (question.replace('Show me the last ', '').replace(' piazza post(s)', '')).replace(' by','').split(' ')
                num_recent = question[0]
                professor = question[1] + " " + question[2]
                total_posts = my_class.iter_all_posts()
                posts_by_professor = []
                for post in total_posts:
                    prof_id = post['history'][0]['uid']
                    prof_name = my_class.get_users([prof_id])[0]['name']
                    if (prof_name == professor):
                        posts_by_professor.append(post)

                print(posts_by_professor)
                all_post_attr = get_post_attr(posts_by_professor)
                for post in all_post_attr:
                    my_text += pretty_print(post)

            else:
                num_recent = (question.replace('Show me the last ', '').replace(' piazza post(s)', '')).split(' ', 2)[1]
                posts = my_class.iter_all_posts(limit=int(num_recent))
                all_post_attr = get_post_attr(posts)

                for post in all_post_attr:
                    my_text += pretty_print(post)

            response = client.chat_postMessage(
                channel=myEvent['channel'],
                text=my_text)
