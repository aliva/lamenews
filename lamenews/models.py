from django.db import models
from django.contrib.auth import get_user_model

class PostManager(models.Manager): 
    def get_recent(self):
        return self.all().order_by('create_date')

class Post(models.Model):
    title = models.CharField(max_length=140,
                             unique=True) 
    content = models.TextField()
    tags = models.ManyToManyField('Tag')
    creator = models.ForeignKey(get_user_model())
    create_date = models.DateTimeField(auto_now_add=True)
    visit_count = models.IntegerField(default=0)
    
    objects = PostManager()
    
    def __str__(self):
        return self.title 
    
class Tag(models.Model):
    name = models.CharField(max_length=140)
    
    def __str__(self):
        return self.name