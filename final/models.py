from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    scoreSum = models.IntegerField(default=0)
    pass

class Topics(models.Model):
    topic_name = models.CharField(max_length=64)
    def __str__(self):
        return self.topic_name

class Cards(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="owner")
    front_side = models.CharField(max_length=512)
    back_side = models.CharField(max_length=512)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, blank=True, related_name="topic")
    
    def __str__(self):
        return f"{self.owner} created {self.front_side}"

class UserChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    card = models.ForeignKey(Cards, on_delete=models.CASCADE,related_name="card")
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} scored {self.score} for {self.card.front_side}"

