from django.db import models


class Bot(models.Model):
    token = models.CharField(max_length=100)

    @classmethod
    def set_token(cls, token='1175594888:AAFM9ACsHYs5muY3Vs212V_ahc1HCQVFi6c'):
        if cls.objects.count() > 0:
            bot = cls.objects.first()
        else:
            bot = cls.objects.create(token=token)
        return bot.token

    @classmethod
    def get_token(cls):
        return cls.objects.first().token


class User(models.Model):
    name = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)


class Message(models.Model):
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
