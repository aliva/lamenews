from django.db import models
from django.contrib.auth import get_user_model

class Post(models.Model):
    post = models.TextField()
    title = models.CharField(max_length=140,
                             unique=True) 
    tags = models.ManyToManyField('Tag')
    creator = models.ForeignKey(get_user_model())
    create_date = models.DateTimeField(auto_now_add=True) 
    
class Tag(models.Model):
    name = models.CharField(max_length=140)