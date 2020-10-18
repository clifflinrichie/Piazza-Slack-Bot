import os
from piazza_api import Piazza
import html
from bs4 import BeautifulSoup

def get_child_post(children):
    ret = []
    if len(children) == 0:
        return ret
    else:
        for child in children:
            for x in child.keys():
                print(x)
            if "subject" not in child.keys():
                ret.append({
                    'text': child['history'][0]['content'],
                    'children': get_child_post(child['children'])
                })
            else:
                ret.append({
                    'text': child['subject'],
                    'children': get_child_post(child['children'])
                })
        return ret

def get_post_attr(posts):
    all_post_attr = []
    for post in posts:
        all_post_attr.append({ 
            'content' : post['history'][-1]['content'], #most recent post
            'children': get_child_post(post['children'])
        })
    return all_post_attr

def clean_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return html.unescape(soup.get_text())

def pretty_print(post_dict):
    text = ""
    text += ("\n ****************************************** POST ******************************************\n")
    text += ("\*bold\*")
    text += ("*bold*")
    text += (f"```{clean_text(post_dict['content'])}```")
    for comment in post_dict['children']:
        text += (f"\n>```{(clean_text(comment['text']))}```")
        text += ("\n")
        if len(comment['children']) != 0:
            for child_comment in comment['children']:
                text += (f"\n>```{(clean_text(comment['text']))}```")
                text += ("\n")
    text += ("\n")
    return text
