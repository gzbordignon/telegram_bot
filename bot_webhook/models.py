from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
