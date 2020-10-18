import html
from bs4 import BeautifulSoup

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
            'created': post['created'][0:10],
            'content' : post['history'][0]['content'], #most recent post
            'children': get_child_post(post['children'])
        })
        # for i, content in enumerate(post['history']):
        #     print(f"History edit: {i}")
        #     print(clean_text(content['content']))

    
    return all_post_attr


def pretty_print(post_dict):
    text = ""
    text += (f"\n*{clean_text(post_dict['title'])} | Written on {clean_text(post_dict['created'])}*")
    text += (f"```{clean_text(post_dict['content'])}```")
    for comment in post_dict['children']:
        text += (f"\n>```{(clean_text(comment['text']))}```")
        text += ("\n")
        if len(comment['children']) != 0:
            for child_comment in comment['children']:
                text += (f"\n>`{(clean_text(child_comment['text']))}`")
                text += ("\n")
    text += ("\n")
    return text

def pretty_print_instr(post_dict):
    text = ""
    if(any([child['type'] == "Instructor" for child in post_dict['children']])): #are there instructor answers?
        text += (f"*{clean_text(post_dict['title'])} | Written on {clean_text(post_dict['created'])}*\n")
        text += (f"```{clean_text(post_dict['content'])}```")
        for comment in post_dict['children']:
            if comment['type'] == "Instructor":
                text += (f"\n>```{comment['type']}: {(clean_text(comment['text']))}```")
                text += ("\n")
                if len(comment['children']) != 0:
                    for child_comment in comment['children']:
                        text += (f"\n>`{child_comment['type']}: {(clean_text(child_comment['text']))}`")
                        text += ("\n")

    return text if "Instructor" in text else ""
