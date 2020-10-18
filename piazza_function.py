import os
from piazza_api import Piazza
import piazza_api
import html
from bs4 import BeautifulSoup

#os.environ['PIAZZA_USERNAME'] = "nv2ba@virginia.edu"
#os.environ['PIAZZA_PASSWORD'] = "******"

def get_child_post(children):
    ret = []
    if len(children) == 0:
        return ret
    else:
        for child in children:
            child_dict = {}
            if "subject" not in child.keys():
                child_dict['text'] = child['history'][0]['content']
            else:
                child_dict['text'] = child['subject']
            child_dict['type'] = "Instructor" if child['type'] == "i_answer" else "Student"
            child_dict['children'] = get_child_post(child['children'])
            ret.append(child_dict)
        return ret

def clean_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return html.unescape(soup.get_text())

def get_post_attr(posts):
    all_post_attr = []
    for post in posts:
        all_post_attr.append({ 
            'title': post['history'][0]['subject'],
            'content' : post['history'][0]['content'], #most recent post
            'children': get_child_post(post['children'])
        })
        # for i, content in enumerate(post['history']):
        #     print(f"History edit: {i}")
        #     print(clean_text(content['content']))

    
    return all_post_attr


def pretty_print(post_dict):
    text = ""
    text += ("\n ****************************************** POST ******************************************\n")
    text += (f"```{clean_text(post_dict['content'])}```")
    for comment in post_dict['children']:
        text += (f"\n>```{(clean_text(comment['text']))}```")
        text += ("\n")
        if len(comment['children']) != 0:
            for child_comment in comment['children']:
                text += (f"\n>```{(clean_text(child_comment['text']))}```")
                text += ("\n")
    text += ("\n")
    return text

def pretty_print_instr(post_dict):
    text = ""
    text += ("\n ****************************************** POST ******************************************\n")
    if(any([child['type'] == "Instructor" for child in post_dict['children']])): #are there instructor answers?
        text += (f"{clean_text(post_dict['title'])}\n")
        text += (f"```{clean_text(post_dict['content'])}```")
        for comment in post_dict['children']:
            if comment['type'] == "Instructor":
                text += (f"\n>```{comment['type']}: {(clean_text(comment['text']))}```")
                text += ("\n")
                if len(comment['children']) != 0:
                    for child_comment in comment['children']:
                        text += (f"\n>```{child_comment['type']}: {(clean_text(child_comment['text']))}```")
                        text += ("\n")

    return text if "Instructor" in text else ""



if __name__ == "__main__":
    p = Piazza()

    p.user_login(email=os.environ['PIAZZA_USERNAME'], password=os.environ['PIAZZA_PASSWORD'])

    cs2110 = p.network("jzqhh4bax85av")

    max_cid = cs2110.get_statistics()['total']['questions'] - 1
    cid = max_cid
    instr_goal = 10
    num_instr = 0
    text = ""
    iters = 0
    while(num_instr < instr_goal and cid > (max_cid - 25)):
        iters+=1
        try:
            post = cs2110.get_post(cid)
            all_post_attr = get_post_attr([post])
            post_text = pretty_print_instr(all_post_attr[0])
            if post_text != "":
                text+=post_text
                num_instr+=1
        except piazza_api.exceptions.RequestError:
            print(cid)
            pass
        cid-=1
    
    print(text)
    print(f"max: {max_cid}\t cid:{cid}")
    print(iters)

    # num_recent = 7
    # cs2150 = p.network("jzqhh4bax85av")
    
    # # posts = cs2150.iter_all_posts(limit=num_recent)
    # # all_post_attr = get_post_attr(posts)
    
    # all_post_attr = get_post_attr([cs2150.get_post(cid) for cid in range(900, 906)])

    # #post = cs2150.get_post(1090)
    # #all_post_attr = get_post_attr([post])

    # for post in all_post_attr:
    #     pass
    #     #print(pretty_print_i(post))
