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

    return post.id


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

    return comment