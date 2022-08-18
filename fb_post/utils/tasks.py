from fb_post.models import User,Post,Comment,React
from datetime import datetime

def create_post(user_id, post_content):
    """
    :returns: post_id
    """
    try:
        user = User.objects.get(user_id=user_id)

    except:
        print("InvalidUserException")

    post = Post.objects.create(posted_by=user,content=post_content,posted_at=datetime.now())

    return post.post_id


def create_comment(user_id, post_id, comment_content):
    """
    :returns: comment_id
    """
    try:
        user = User.objects.get(user_id=user_id)
    except:
        post = Post.objects.get(post_id = post_id)

    comment = Comment.objects.create(content=comment_content,commented_at=datetime.now(),commented_by=user,post=post)

    comment.save()

    return comment.comment_id

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
    react = React.objects.create(reacted_at=datetime.now(),reacted_by=user_id,post=post,react =reaction_type)