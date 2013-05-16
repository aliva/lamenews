from django.db import models
from django.contrib.auth import get_user_model

class PostManager(models.Manager): 
    def get_recent(self):
        return self.all().order_by('-create_date')
    def get_top(self):
        return self.all().order_by('-visit_count')

class Post(models.Model):
    title = models.CharField(max_length=140,
                             unique=True) 
    content = models.TextField()
    tags = models.ManyToManyField('Tag')
    creator = models.ForeignKey(get_user_model())
    create_date = models.DateTimeField(auto_now_add=True)
    visit_count = models.IntegerField(default=0)
    
    vote_ups = models.IntegerField(default=0)
    vote_downs = models.IntegerField(default=0)
    
    objects = PostManager()
    
    def __str__(self):
        return self.title 
    
class Tag(models.Model):
    name = models.CharField(max_length=140,unique=True)
    
    def __str__(self):
        return self.name
    
class Votes(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey(get_user_model())
    
    VOTE_CHOICES = (
        ('up',  1),
        ('no',  0),
        ('dn', -1),
    )
    vote = models.SmallIntegerField(choices=VOTE_CHOICES, default='no')