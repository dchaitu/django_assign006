from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    profile_pic= models.TextField()


class Post(models.Model):
    content = models.CharField(max_length=1000)
    posted_at = models.DateTimeField()
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    commented_at = models.DateTimeField()
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    # reply = models.ForeignKey(Comment)

class React(models.Model):
    CHOICES=(
    ("WOW","WOW"),
    ("LIT","WOW"),
    ("LOVE","LOVE"),
    ("HA","HAHA"),
    ("UP","THUMBS - UP"),
    ("DOWN","THUMBS - DOWN"),
    ("ANGRY","ANGRY"),
    ("SAD","SAD"),
)
    react = models.CharField(choices=CHOICES,max_length=20)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    reaction = models.CharField(max_length=100)
    reacted_at = models.DateTimeField()
    reacted_by = models.ForeignKey(User,on_delete=models.CASCADE)




