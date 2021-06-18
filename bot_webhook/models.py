from django.db import models
import requests


class Bot(models.Model):
    token = models.CharField(max_length=100)

    @classmethod
    def set_token(cls, token='1175594888:AAFM9ACsHYs5muY3Vs212V_ahc1HCQVFi6c'):
        if cls.objects.count() > 0:
            bot = cls.objects.first()
            if token is not None:
                bot.token = token
                bot.save()
        else:
            bot = cls.objects.create(token=token)
        return bot.token

    @classmethod
    def get_token(cls):
        return cls.objects.first().token

    @classmethod
    def create_message(cls, user_id, text):
        user = User.objects.get(pk=user_id)
        bot = cls.objects.first()
        bot.objects.create(sent_to=user, text=text)

    @classmethod
    def send_message(cls, token, chat_id, text, reply_markup=None):
        url = 'https://api.telegram.org/bot' + token + '/sendMessage'
        data = dict(chat_id=chat_id, text=text, reply_markup=reply_markup)
        requests.post(url, data)


class User(models.Model):
    name = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)


class Message(models.Model):
    sent_by = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='messages')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
