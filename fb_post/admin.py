from django.contrib import admin
from fb_post.models import User,Post,Comment,React,Group,Membership
from fb_post.utils.enum import ReactionType

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(React)
admin.site.register(Group)
admin.site.register(Membership)

