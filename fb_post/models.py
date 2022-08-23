from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_pic = models.TextField()

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return f'{self.name}'


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_membership')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'Membership for {self.group.name}'


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    posted_at = models.DateField(auto_now=False, auto_now_add=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return "{} Posted {}".format(self.posted_by.name, self.content)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    commented_at = models.DateField(auto_now=False, auto_now_add=False)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, related_name="commenter", on_delete=models.CASCADE, blank=True, null=True)
    reply = models.ForeignKey('self', related_name="reply_to_comment", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.reply:
            return "{} replied {}".format(self.commented_by.name, self.content)
        else:
            return "{} commented on {}".format(self.commented_by.name, self.post.content)


class React(models.Model):
    CHOICES = (
        ("WOW", "WOW"),
        ("LIT", "LIT"),
        ("LOVE", "LOVE"),
        ("HA", "HAHA"),
        ("THUMBS - UP", "UP"),
        ("THUMBS - DOWN", "DOWN"),
        ("ANGRY", "ANGRY"),
        ("SAD", "SAD"),
    )
    reaction = models.CharField(choices=CHOICES, max_length=100)
    post = models.ForeignKey(Post, related_name="reacted_to_post", on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, related_name="commented_to_the_post", on_delete=models.CASCADE, blank=True,
                                null=True)
    reacted_at = models.DateField(auto_now=False, auto_now_add=False)
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Feeling {} by {}".format(self.reaction, self.reacted_by.name)
