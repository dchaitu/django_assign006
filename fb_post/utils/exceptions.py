from django.core.exceptions import *
from fb_post.models import User, Post, Comment, React,Group,Membership


class InvalidUserException(User.DoesNotExist):
     pass

class InvalidGroupNameException(Group.DoesNotExist):
    pass

class InvalidMemberException(Membership.DoesNotExist):
    pass

class InvalidPostContent(Post.DoesNotExist):
    pass

class InvalidGroupException(Group.DoesNotExist):
    pass

class UserIsNotAdminException(PermissionDenied):
    pass

class UserNotInGroupException(User.DoesNotExist):
    pass

class InvalidPostException(Post.DoesNotExist):
    pass

class InvalidCommentException(Comment.DoesNotExist):
    pass

class InvalidCommentContent(Comment.DoesNotExist):
    pass

class InvalidReplyContent(Comment.DoesNotExist):
    pass

class InvalidReactionTypeException(React.DoesNotExist):
    pass

class UserCannotDeletePostException(PermissionDenied):
    pass