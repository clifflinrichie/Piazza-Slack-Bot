import os
from piazza_api import Piazza


os.environ['PIAZZA_USERNAME'] = "nv2ba@virginia.edu"
os.environ['PIAZZA_PASSWORD'] = "*********"

def get_child_post(children):
    ret = []
    if len(children) == 0:
        return ret
    else:
        for child in children:
            if "subject" not in child.keys():
                ret.append({
                    'text': child['subject'],
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

def pretty_print(post_dict):
    print("\n ****************************************** NEW POST ******************************************\n")
    print(f"Main: {post_dict['content']}")
    print("\n**************************\n")
    for comment in post_dict['children']:
        print(f"\tComment: {comment['text']}")
        print("\n**************************\n")
        if len(comment['children']) != 0:
            for child_comment in comment['children']:
                print(f"\t\tComment: {child_comment['text']}")
                print("\n**************************\n")


if __name__ == "__main__":
    p = Piazza()

    p.user_login(email=os.environ['PIAZZA_USERNAME'], password=os.environ['PIAZZA_PASSWORD'])

    num_recent = 4
    cs2150 = p.network("k5bqcfbzltk49c")
    posts = cs2150.iter_all_posts(limit=num_recent)

    all_post_attr = get_post_attr(posts)

    for post in all_post_attr:
        pretty_print(post)