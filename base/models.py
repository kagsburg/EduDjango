from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    #room attributes
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #a room can have one topic
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    #auto_now_add=True for first time creation
    #auto_now=True for every update
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    #Room is parent thus one to many relationship on delete of room all messages are deleted
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    # handle = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]