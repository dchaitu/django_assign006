from django.db.models import Q, Count, Avg
from fb_post.models import User, Post, Comment, React
from datetime import date
from fb_post.utils.exceptions import InvalidUserException, InvalidPostContent, InvalidCommentException, \
    InvalidPostException, InvalidCommentContent, InvalidReplyContent, InvalidReactionTypeException, \
    UserCannotDeletePostException
from fb_post.utils.enum import ReactionType
from datetime import datetime


def create_post(user_id, post_content):
    """
    :returns: post_id
    """
    post = {}
    try:
        user = User.objects.get(user_id=user_id)
        if not user:
            raise InvalidUserException

        if len(post_content) == 0:
            raise InvalidPostContent("Post has no content")

    except InvalidPostContent:
        print("Post has no content")

    except InvalidUserException:
        print("User id is not defined")

        date_entry = input('Enter a date in YYYY-MM-DD format')
        year, month, day = map(int, date_entry.split('-'))
        posted_at = date(year, month, day)
        post = Post.objects.create(posted_by=user, content=post_content, posted_at=posted_at)
        post.save()

    return post


def create_comment(user_id, post_id, comment_content):
    """
    :returns: comment_id
    """
    comment = {}
    try:
        user = User.objects.get(user_id=user_id)
        if not user:
            raise InvalidUserException

        post = Post.objects.get(post_id=post_id)
        if not post:
            raise InvalidPostException

        if len(comment_content) == 0:
            raise InvalidCommentContent


    except InvalidPostException:
        print("Post id not in database")

    except InvalidCommentContent:
        print("Comment id is not defined")

    except InvalidUserException:
        print("User id is not defined")

        post.save()
        date_entry = input('Enter a date in YYYY-MM-DD format')
        year, month, day = map(int, date_entry.split('-'))
        commented_time = date(year, month, day)
        comment = Comment.objects.create(content=comment_content, commented_at=commented_time, commented_by=user,
                                         post=post)

        comment.save()

    return comment


def reply_to_comment(user_id, comment_id, reply_content):
    """
    :returns: comment_id
    """
    try:
        user = User.objects.get(user_id=user_id)
        if not user:
            raise InvalidUserException
        comment = Comment.objects.get(comment_id=comment_id)
        if not comment:
            raise InvalidCommentException

        if len(reply_content) == 0:
            raise InvalidReplyContent

    # Additionally , if the given comment_id corresponds to a 'reply' instead of a direct comment to a post, then a reply should be created to the comment

    except InvalidUserException:
        print("User id is not defined")

    except InvalidCommentException:
        print("Comment id is not defined")

        # check_comment = Comment.objects.get(comment_id=comment_id)
        # if check_comment.reply:
        #     Comment.objects.create(commented_by=user, content=reply_content, comment_id=comment_id)

    reply = Comment.objects.create(commented_by=user, content=reply_content, reply_id=comment_id,
                                   commented_at=datetime.now().strftime("%Y-%m-%d"))
    reply.save()

    return reply.comment_id


def react_to_post(user_id, post_id, reaction_type):
    """
    """
    try:
        user = User.objects.get(user_id=user_id)
        if not user:
            raise InvalidUserException
        post = Post.objects.get(post_id=post_id)
        if not post:
            raise InvalidPostException
        reacted_time = datetime.now().strftime("%Y-%m-%d")
        if reaction_type not in [ReactionType.WOW.value, ReactionType.HA.value, ReactionType.UP.value,
                                 ReactionType.ANGRY.value,
                                 ReactionType.LIT.value, ReactionType.DOWN.value, ReactionType.SAD.value,
                                 ReactionType.LOVE.value]:
            raise InvalidReactionTypeException
        # if the user is reacting to the post for the first time, then the function should create a reaction.
        already_reacted = React.objects.filter(reacted_by=user_id, post=post)
        if already_reacted:
            already_reacted.delete()
        react = React.objects.create(reacted_at=reacted_time, reacted_by=user, post=post, reaction=reaction_type)
        react.save()
    except InvalidPostException:
        print("Post id is not defined")

    except InvalidUserException:
        print("User id is not defined")

    except InvalidReactionTypeException:
        print("Reaction Type is not defined")


def react_to_comment(user_id, comment_id, reaction_type):
    """
    """
    try:
        user = User.objects.get(user_id=user_id)
        if not user:
            raise InvalidUserException
        comment = Comment.objects.get(comment_id=comment_id)
        if not comment:
            raise InvalidCommentException
        if reaction_type not in [ReactionType.WOW.value, ReactionType.HA.value, ReactionType.UP.value,
                                 ReactionType.ANGRY.value,
                                 ReactionType.LIT.value, ReactionType.DOWN.value, ReactionType.SAD.value,
                                 ReactionType.LOVE.value]:
            raise InvalidReactionTypeException
        reaction_exists = React.objects.get(comment=comment, reacted_by=user)
        if reaction_exists.reaction == reaction_type:
            reaction_exists.delete()
        elif reaction_exists.reaction != reaction_type:
            reaction_exists.reaction = reaction_type
            reaction_exists.reacted_at = datetime.now().strftime("%Y-%m-%d")
            reaction_exists.save()
        else:
            React.objects.create(reaction=reaction_type, comment=comment, reacted_by=user,
                                 reacted_at=datetime.now().strftime("%Y-%m-%d"))


    except InvalidUserException:
        print("User id is not defined")

    except InvalidReactionTypeException:
        print("Reaction Type is not defined")


def get_total_reaction_count():
    r = React.objects.count()
    return r


def get_reaction_metrics(post_id):
    """Return total count for each reaction type"""
    try:
        post = Post.objects.get(pk=post_id)
        if not post:
            raise InvalidPostException
        love = Q(reaction=ReactionType.LOVE.value)
        lit = Q(reaction=ReactionType.LIT.value)
        up = Q(reaction=ReactionType.UP.value)
        down = Q(reaction=ReactionType.DOWN.value)
        wow = Q(reaction=ReactionType.WOW.value)
        sad = Q(reaction=ReactionType.SAD.value)
        angry = Q(reaction=ReactionType.ANGRY.value)
        post = Q(post=post)

        d = {"Love": React.objects.filter(post & love).count(),
             "LIT": React.objects.filter(post & lit).count(),
             "UP": React.objects.filter(post & up).count(),
             "DOWN": React.objects.filter(post & down).count(),
             "Wow": React.objects.filter(post & wow).count(),
             "Sad": React.objects.filter(post & sad).count(),
             "Angry": React.objects.filter(post & angry).count()}

    except InvalidPostException:
        print("post id is defined")

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
        if not user:
            raise InvalidUserException
        post = Post.objects.get(pk=post_id)
        if not post:
            raise Exception('InvalidPostException')

        if post.posted_by == user:
            # reaction = React.objects.filter(react_to_post=post).delete()
            # comments = Comment.objects.filter(commented_to_the_post=post).delete()

            post.delete()
            print(f"post No {post_id} deleted and comments and reactions to it also deleted")

    except UserCannotDeletePostException:
        print("Post is not created by user")
    except InvalidUserException:
        print("User id is not defined")


# Need to check
def get_posts_with_more_positive_reactions():
    """
    """
    l=[]
    positive = [ReactionType.WOW.value, ReactionType.LOVE.value, ReactionType.LIT.value, ReactionType.HA.value, ReactionType.UP.value]
    negative = [ReactionType.DOWN.value, ReactionType.ANGRY.value, ReactionType.SAD.value]
    posts = Post.objects.all()
    # posr = Q(Count(reaction__in=positive))
    # negr = Q(Count(reaction__in=negative))
    for post in posts:
        if(post.reacted_to_post.filter(reaction__in=positive).count()>post.reacted_to_post.filter(reaction__in=negative).count()):
            l.append(post)

    # for post in posts:
    #     if posr>negr:
    #         l.append(post)

    return l


# check

def get_posts_reacted_by_user(user_id):
    """
    :returns: list of post ids
    """
    user = User.objects.get(user_id=user_id)
    reacted_posts = React.objects.filter(reacted_by=user)
    post_ids = Post.objects.filter(post_id__in=reacted_posts).values('post_id')

    return list(post_ids)


def get_reactions_to_post(post_id):
    """
    :returns: [
        {"user_id": 1, "name": "iB Cricket", "profile_pic": "", "reaction": "LIKE"},
        ...
    ]
    """
    try:
        post = Post.objects.get(post_id=post_id)
        reactions = React.objects.filter(post=post)

        react_list = []

        for r in reactions:
            react_dict = {}
            react_dict['user_id'] = r.reacted_by_id
            react_dict['name'] = r.reacted_by.name
            react_dict['profile_pic'] = r.reacted_by.profile_pic
            react_dict['reaction'] = r.reaction
            react_list.append(react_dict)

    except (Post.DoesNotExist, Post.MultipleObjectsReturned):
        print("Post may be deleted or not created")
        react_list = []
        return react_list

    return react_list

# Exceptions not working properly
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
    try:

        post = Post.objects.get(pk=post_id)
        if not post:
            raise InvalidPostException
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
                r = {"comment_id": y.reply.comment_id,
                     "commenter": {
                         "user_id": y.commented_by.user_id,
                         "name": y.commented_by.name,
                         "profile_pic_url": y.commented_by.profile_pic
                     },
                     "commented_at": y.commented_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
                     "comment_content": y.content,
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
    except InvalidPostException:
        print("post id doesn't exist")

    except (Post.DoesNotExist, Post.MultipleObjectsReturned):
        print("Post may be deleted")
        react_list = []
        return react_list


def get_user_posts(user_id):
    """
    Explanation: Return a list of responses similar to get_post
    """
    posts = Post.objects.filter(posted_by=user_id)
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
        if not comment:
            raise InvalidCommentException
        reply = Comment.objects.filter(reply=comment)
        if reply is None:
            raise Comment.DoesNotExist
        for y in reply:
            r = {"comment_id": y.reply.comment_id,
                 "commenter": {
                     "user_id": y.commented_by.user_id,
                     "name": y.commented_by.name,
                     "profile_pic_url": y.commented_by.profile_pic
                 },
                 "commented_at": y.commented_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
                 "comment_content": y.content,

                 }
            replies.append(r)
    except InvalidCommentException:
        print("Comment is not created")

    except (Comment.DoesNotExist, Comment.MultipleObjectsReturned):
        print("Comment may be deleted")

    return replies
