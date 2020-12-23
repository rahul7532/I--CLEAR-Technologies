from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    age = models.IntegerField()


class Connected(models.Model):
    first = models.ForeignKey(AppUser, related_name='first', on_delete=models.CASCADE)
    second = models.ForeignKey(AppUser, related_name='second', on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(AppUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(AppUser, related_name='receiver', on_delete=models.CASCADE)
    data = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


