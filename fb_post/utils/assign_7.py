from fb_post.models import User, Post, Comment, React, Group, Membership
from datetime import date
from fb_post.utils.enum import ReactionType

from fb_post.utils.exceptions import InvalidUserException,UserNotInGroupException, UserIsNotAdminException, InvalidGroupNameException, \
    InvalidMemberException, \
    InvalidGroupException


def create_group(user_id, name, member_ids):
    try:
        user = User.objects.get(user_id=user_id)
        if user is None:
            raise InvalidUserException

        if len(name) == 0:
            raise InvalidGroupNameException

        group = Group.objects.create(members=user, name=name)
        group.save()

        for id in member_ids:
            member = Membership.objects.get(id=id)
            if not member:
                raise InvalidMemberException

    except InvalidUserException:
        print("User id is not defined")

    except InvalidGroupNameException:
        print("Game doesn't have name")

    except InvalidMemberException:
        print("Members are not present in db")

    return group.id


def add_member_to_group(user_id, new_member_id, group_id):
    try:
        user = User.objects.get(user_id=user_id)
        if not user:
            raise InvalidUserException
        member = User.objects.get(user_id=new_member_id)
        if not member:
            raise InvalidMemberException
        group = Group.objects.get(id=group_id)
        if not group:
            raise InvalidGroupException

        check_admin = Membership.objects.get(member_id=user_id).is_admin

        if not check_admin:
            raise UserIsNotAdminException

        if member not in group.members.all():
            group.members.add(member)

    except InvalidUserException:
        print("User id is not defined")

    except InvalidGroupException:
        print("Game doesn't have name")

    except InvalidMemberException:
        print("Members are not present in db")

    except UserIsNotAdminException:
        print("User is not an admin")


def remove_member_from_group(user_id, member_id, group_id):
    try:
        user = User.objects.get(user_id=user_id)
        if user is None:
            raise InvalidUserException
        member = User.objects.get(user_id=member_id)
        if member:
            raise InvalidMemberException
        group = Group.objects.get(id=group_id)
        if group:
            raise InvalidGroupException
        group.members.remove(member)

        check_admin = Membership.objects.get(user_id=user_id).is_admin

        if check_admin:
            raise UserIsNotAdminException

    except InvalidUserException:
        print("User id is not defined")

    except InvalidGroupNameException:
        print("Game doesn't have name")

    except InvalidMemberException:
        print("Members are not present in db")

    except UserIsNotAdminException:
        print("User is not an admin")

def make_member_as_admin(user_id, member_id, group_id):
    try:
        user = User.objects.get(user_id=user_id)
        if user is None:
            raise InvalidUserException
        member = Group.objects.get(members__user_id=member_id)
        if member:
            raise InvalidMemberException
        group = Group.objects.get(id=group_id)
        if not user or not member:
            raise UserNotInGroupException
        group.membership_set.update(is_admin=True)
    except InvalidUserException:
        print("User id is not defined")

    except InvalidGroupNameException:
        print("Game doesn't have name")

    except InvalidMemberException:
        print("Members are not present in db")

    except UserNotInGroupException:
        print("User not in group")

def create_post(user_id, post_content, group_id=None):
    """
    :returns: post_id
    """
    user = User.objects.get(user_id=user_id)
    user.save()
    group = Group.objects.get(pk=group_id)
    post_id = input("post id")
    date_entry = input('Enter a date in YYYY-MM-DD format')
    year, month, day = map(int, date_entry.split('-'))
    posted_at = date(year, month, day)
    group.post_set.create(post_id=post_id, content=post_content, posted_at=posted_at, posted_by=user)
    group.save()


def get_group_feed(user_id, group_id, offset, limit):
    """
    :return: [
    {
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
    ]
    """
    all_posts = []
    user = User.objects.get(user_id=user_id)
    group = Group.objects.get(pk=group_id)
    if user in group.members.all():
        posts = Post.objects.filter(posted_by=user)

        for post in posts:
            post_obj = {}
            post.update({"post_id": post.post_id})
            user_obj = {"name": post.posted_by.name, "user_id": post.posted_by.user_id,
                        "profile_pic": post.posted_by.profile_pic}
            post.update({"posted_by": user_obj})
            post.update({"posted_at": post.posted_at, "post_content": post.content})
            # "reactions": {
            #     "count": 10,
            #     "type": ["HAHA", "WOW"]
            # },
            react_obj = {}
            try:
                reactions = React.objects.filter(post=post)
            except:
                reactions = []
            all_types = []
            for react in reactions:
                all_types.append(react.reaction_type)

            react_obj.update({"reactions": {"count": reactions.count(), "type": all_types}})
            comments = Comment.objects.filter(post=post)
            comments_count = Comment.objects.filter(post=post).count()
            all_comments = []

            for comment in comments:
                comment_obj = {}
                comment_obj.update({"comment_id": comment.comment_id,
                                    "commenter": {"user_id": comment.commented_by.user_id,
                                                  "name": comment.commented_by.name,
                                                  "profile_pic": comment.commented_by.profile_pic},
                                    "commented_at": comment.commented_at, "comment_content": comment.content})
                all_comments.append(comment_obj)

            react_obj.update({"comments": all_comments})
            react_obj.update({"comments_count": comments_count})
            post_obj.update(react_obj)
            all_posts.append(post_obj)
    return all_posts[offset:offset + limit]


def get_posts_with_more_comments_than_reactions():
    """
    :returns: list of post_ids
    """
    all_posts = []
    posts = Post.objects.all()
    for post in posts:
        comment_count = (Comment.objects.filter(post=post).count())
        react_count = React.objects.filter(post=post).count()
        if (comment_count > react_count):
            all_posts.append(post.post_id)

    return all_posts


def get_posts_with_more_positive_reactions(user_id):
    """
    List all posts which have more Positive (Like, Love, Haha, Wow) reaction than Negative (Sad, Angry)
    """
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(posted_by=user)
    positive_posts = []
    for post in posts:
        reactions = React.objects.filter(post=post)
        positive_count = 0
        negative_count = 0
        for reaction in reactions:

            if reaction.reaction_type in [ReactionType.WOW.value, ReactionType.LIT.value, ReactionType.LOVE.value, ReactionType.HA.value, ReactionType.UP.value]:
                positive_count += 1
            elif reaction.reaction_type in [ReactionType.SAD.value, ReactionType.ANGRY.value, ReactionType.DOWN.value]:
                negative_count += 1
        if positive_count > negative_count:
            positive_posts.append(post)

    return positive_posts


def get_silent_group_members(group_id):
    """
    """
    group = Group.objects.get(id=group_id)
    users = group.members.all()
    silent_users = []
    for user in users:
        if (Post.objects.filter(posted_by=user).count() == 0):
            silent_users.append(user)

    return silent_users


def get_user_posts(user_id):
    """
    :return: [
    {
        "post_id": 1,
        "group": {
            "group_id": 1,
            "name": "Group Name"
        },
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
    ]
    """
    user = User.objects.get(user_id=user_id)
    posts = Post.objects.filter(posted_by=user)
    all_posts = []
    for post in posts:
        post_obj = {}
        group_obj = {}
        post_obj.update({"post_id": post.post_id})
        group_obj.update({"group_id": post.group.id, "name": post.group.name})
        post_obj.update({"group": group_obj})
        post_obj.update({"posted_by": {"name": post.posted_by.name, "user_id": post.posted_by.user_id,
                                       "profile_pic": post.posted_by.profile_pic}})
        post_obj.update({"posted_at": post.posted_at, "post_content": post.content})
        post_obj.update({})
        try:
            reactions = React.objects.filter(post=post)
        except:
            reactions = []
        all_types = []
        for react in reactions:
            all_types.append(react.reaction_type)

        post_obj.update({"reactions": {"count": reactions.count(), "type": all_types}})
        comments = Comment.objects.filter(post=post)
        comments_count = Comment.objects.filter(post=post).count()
        all_comments = []
        # "replies": [{
        #     "comment_id": 2
        #     "commenter": {
        #         "user_id": 1,
        #         "name": "iB Cricket",
        #         "profile_pic": "https://dummy.url.com/pic.png"
        #     },
        for comment in comments:
            comment_obj = {}
            all_replies = []

            replies = Comment.objects.filter(reply__comment_id=comment.comment_id)
            replies_count = Comment.objects.filter(reply__comment_id=comment.comment_id).count()
            for reply in replies:
                reply_obj = {}
                reply_obj.update({"comment_id": reply.comment_id})
                commenter_obj = {}
                commenter_obj.update({"user_id": reply.commented_by.user_id, "name": reply.commented_by.name,
                                      "profile_pic": reply.commented_by.profile_pic})
                reply_obj.update({"commenter": commenter_obj})
                reply_obj.update({"commented_at": reply.commented_at, "comment_content": reply.content})
                reply_reactions = React.objects.filter(comment=reply)
                all_reply_types = []
                for react in reply_reactions:
                    all_reply_types.append(react.reaction_type)
                reply_obj.update({"reactions": {"count": reactions.count(), "type": all_types}})
                all_replies.append(reply_obj)

            comment_obj.update({"comment_id": comment.comment_id,
                                "commenter": {"user_id": comment.commented_by.user_id,
                                              "name": comment.commented_by.name,
                                              "profile_pic": comment.commented_by.profile_pic},
                                "commented_at": comment.commented_at,
                                "comment_content": comment.content})
            comment_obj.update({"replies_count": replies_count, "replies": all_replies})

            all_comments.append(comment_obj)

        post_obj.update({"comments": all_comments})
        post_obj.update({"comments_count": comments_count})
        all_posts.append(post_obj)
        return all_posts
