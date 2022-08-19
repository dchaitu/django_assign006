from fb_post.models import User,Post,Comment,React
from datetime import date

def create_post(user_id, post_content):
    """
    :returns: post_id
    """
    try:
        user = User.objects.get(user_id=user_id)

    except:
    # raise Exception("Sorry, no numbers below zero")
        print("InvalidUserException")
    date_entry = input('Enter a date in YYYY-MM-DD format')
    year, month, day = map(int, date_entry.split('-'))
    posted_at = date(year, month, day)
    post = Post.objects.create(posted_by=user,content=post_content,posted_at = posted_at)
    post.save()

    return post


def create_comment(user_id, post_id, comment_content):
    """
    :returns: comment_id
    """
    try:
        user = User.objects.get(user_id=user_id)
    except:
        print("Not Worked")

    post = Post.objects.get(post_id = post_id)
    post.save()
    date_entry = input('Enter a date in YYYY-MM-DD format')
    year, month, day = map(int, date_entry.split('-'))
    commented_time = date(year, month, day)
    comment = Comment.objects.create(content=comment_content,commented_at=commented_time,commented_by=user,post=post)

    comment.save()

    return comment

def reply_to_comment(user_id, comment_id, reply_content):
    """
    :returns: comment_id
    """
    user = User.objects.get(user_id=user_id)
    reply = Comment.objects.create(commented_by=user,content=reply_content,comment_id=comment_id)
    reply.save()

def react_to_post(user_id, post_id, reaction_type):
    """
    """

    post = Post.objects.get(post_id= post_id)
    date_entry = input('Enter a date in YYYY-MM-DD format')
    year, month, day = map(int, date_entry.split('-'))
    reacted_time = date(year, month, day)
    react = React.objects.create(reacted_at=reacted_time,reacted_by=user_id,post=post,react =reaction_type)
    react.save()


def react_to_comment(user_id, comment_id, reaction_type):
    """
    """
    user = User.objects.get(user_id=user_id)
    comment = Comment.objects.get(comment_id=comment_id)
    reaction = React.objects.filter()

def get_total_reaction_count():
    r = React.objects.count()
    return r


def get_reaction_metrics(post_id):
    """Return total count for each reaction type"""
    try:
        post = Post.objects.get(pk=post_id)
        reactions = React.objects.filter(reacted_by=post)
        d = {"Love": reactions.filter(reaction_type="Love").count(), "Wow": reactions.filter(reaction_type="Wow").count(),
             "Sad": reactions.filter(reaction_type="Sad").count(), "Angry": reactions.filter(reaction_type="Angry").count()}
    except (Post.DoesNotExist, Post.MultipleObjectsReturned):
        print("Post may be deleted")
        react_list = []
        return react_list
    return d


def delete_post(user_id, post_id):
    """
    """
    try:
        user = User.objects.get(user_id=user_id)
        post = Post.objects.get(pk=post_id)
        if post:
            raise Exception('InvalidPostException')

        if post.posted_by == user:

            # reaction = React.objects.filter(react_to_post=post).delete()
            # comments = Comment.objects.filter(commented_to_the_post=post).delete()

            post.delete()
            print("post No {} deleted and comments and reactions to it also deleted".format(post_id))

    except:
        raise Exception('UserCannotDeletePostException')

# Need to check
def get_posts_with_more_positive_reactions():
    """
    """

    reactions = React.objects.all()
    l = []
    for i in reactions:
        if i.reaction != "Sad" or i.reaction != "Angry":
            l.append(i.reacted_to_post)

    return l
# check

def get_posts_reacted_by_user(user_id):
    """
    :returns: list of post ids
    """
    user = User.objects.get(user_id=user_id)
    reacted_posts = React.objects.filter(reacted_by=user)
    l = []
    for r in reacted_posts:
        if r.reacted_to_post:
            l.append(r.reacted_to_post.post_id)

    return l



def get_reactions_to_post(post_id):
    """
    :returns: [
        {"user_id": 1, "name": "iB Cricket", "profile_pic": "", "reaction": "LIKE"},
        ...
    ]
    """
    try:
        post = Post.objects.get(post_id=post_id)
        reactions = React.objects.filter(reacted_to_post=post)

        react_list = []

        for r in reactions:
            react_dict = {}
            react_dict['user_id'] = r.reacted_by_id
            react_dict['name'] = r.reacted_by.name
            react_dict['profile_pic'] = r.reacted_by.profile_pic
            react_dict['reaction'] = r.reaction
            react_list.append(react_dict)

    except (Post.DoesNotExist, Post.MultipleObjectsReturned):
        print("Post may be deleted")
        react_list = []
        return react_list

    return react_list

def get_post(post_id):
    """
    :returns: {
        "post_id": 1,
        "posted_by": {
            "name": "iB Cricket",
            "user_id": 1,
            "profile_pic": "https://dummy.url.com/pic.png"
        },
        "posted_at": "2019-05-21 20:21:46.810366"
        "post_content": "Write Something here...",
        "reactions": {
            "count": 10,
            "type": ["HAHA", "WOW"]
        },
        "comments": [
            {
                "comment_id": 1
                "commenter": {
                    "user_id": 2,
                    "name": "Yuri",
                    "profile_pic": "https://dummy.url.com/pic.png"
                },
                "commented_at": "2019-05-21 20:22:46.810366",
                "comment_content": "Nice game...",
                "reactions": {
                    "count": 1,
                    "type": ["LIKE"]
                },
                "replies_count": 1,
                "replies": [{
                    "comment_id": 2
                    "commenter": {
                        "user_id": 1,
                        "name": "iB Cricket",
                        "profile_pic": "https://dummy.url.com/pic.png"
                    },
                    "commented_at": "2019-05-21 20:22:46.810366",
                    "comment_content": "Thanks...",
                    "reactions": {
                        "count": 1,
                        "type": ["LIKE"]
                    },
                }]
            },
            ...
        ],
        "comments_count": 3,
    }
    """
    post = Post.objects.get(post_id=post_id)
    try:

        post = Post.objects.get(pk=post_id)
        author = post.posted_by
        reactions = React.objects.filter(post=post)
        comments = Comment.objects.filter(post=post)
        # all_reactions = React.objects.all()
        count = 0
        reaction_type = []
        c = []
        replies = []
        for i in comments:
            reacted_to_comment = React.objects.filter(comment=i)
            m = Comment.objects.filter(reply=i)
            for y in m:
                r = {"comment_id": y.replied_to_comment_id,
                     "commenter": {
                         "user_id": y.commented_by.user_id,
                         "name": y.commented_by.name,
                         "profile_pic_url": y.commented_by.profile_pic
                     },

                     }
                replies.append(r)

            for x in reacted_to_comment:
                reaction_type.append(x.reaction)

            d = {"commenter": {"user_id": i.commented_by.user_id, "name": i.commented_by.name,
                               "profile_pic_url": i.commented_by.profile_pic},
                 "commented_at": i.commented_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
                 "comment_content": i.content,
                 "reactions": {"count": React.objects.filter(comment=i).count(), "type": reaction_type},
                 "replies": replies,
                 "replies_count": Comment.objects.filter(reply=i).count()

                 }
            reaction_type = []
            count += len(replies)
            replies = []
            c.append(d)

        l = []
        for r in reactions:
            l.append(r.reaction)

        m = {"post_id": post_id,
             "posted_by":
                 {
                     'name': author.name, 'user_id': author.user_id, 'profile_pic_url': author.profile_pic},
             'posted_at': post.posted_at.strftime('%Y-%m-%d %H:%M:%S.%f'), 'post_content': post.content,
             'reactions': {'count': reactions.count(), 'type': l},
             'comments': c,
             'comments_count': int(len(c) + count)

             }

        return m
    except (Post.DoesNotExist, Post.MultipleObjectsReturned):
        print("Post may be deleted")
        react_list = []
        return react_list


def get_user_posts(user_id):
    """
    Explanation: Return a list of responses similar to get_post
    """
    posts = Post.objects.filter(posted_at=user_id)
    return posts


def get_replies_for_comment(comment_id):
    """
    :returns: [{
        "comment_id": 2
        "commenter": {
            "user_id": 1,
            "name": "iB Cricket",
            "profile_pic": "https://dummy.url.com/pic.png"
        },
        "commented_at": "2019-05-21 20:22:46.810366",
        "comment_content": "Thanks...",
    }]
    """
    replies = []
    try:

        comment = Comment.objects.get(pk=comment_id)
        reply = Comment.objects.filter(replied_to_comment=comment)
        for y in reply:
            r = {"comment_id": y.replied_to_comment_id,
                 "commenter": {
                     "user_id": y.written_by_id,
                     "name": y.written_by.name,
                     "profile_pic_url": y.written_by.profile_pic
                 },
                 "commented_at": y.commented_at_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                 "comment_content": y.comment,

                 }
            replies.append(r)
    except (Comment.DoesNotExist, Comment.MultipleObjectsReturned):

        print("Comment may be deleted")
        replies = []
        return replies

    return replies

