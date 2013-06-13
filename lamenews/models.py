from django.db import models
from django.contrib.auth import get_user_model

class PostManager(models.Manager):
    def get_recent(self):
        return self.all().order_by('-create_date')
    def get_most_visited(self):
        return self.all().order_by('-visit_count')
    def get_most_upvoted(self):
        return self.all().order_by('-vote_ups')

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
    vote = models.SmallIntegerField(choices=VOTE_CHOICES, default=0)

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
    vote_total = models.IntegerField(default=0)

    objects = PostManager()

    def __str__(self):
        return self.title

    def vote_post(self, user, value):
        if Votes.objects.filter(post=self, user=user).exists():
            return 'already voted'

        if value == 'up':
            value = 1
            self.vote_ups +=1
        else:
            value = -1
            self.vote_downs += 1
        self.vote_total = self.vote_ups - self.vote_downs

        Votes.objects.create(post=self, user=user, vote=value)
        self.save()
        return 'done'

class Comment(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey(get_user_model())
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
