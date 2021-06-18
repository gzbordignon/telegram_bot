import requests
from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Message, User, Bot

logger = get_task_logger(__name__)


@shared_task
def send_message(token, chat_id, text, reply_markup=None):
    url = 'https://api.telegram.org/bot' + token + '/sendMessage'
    data = dict(chat_id=chat_id, text=text, reply_markup=reply_markup)
    requests.post(url, data)


@shared_task
def create_message(token, user_id, text):
    bot = Bot.objects.filter(token=token).first()
    user = User.objects.get(pk=user_id)
    Message.objects.create(sent_by=bot, sent_to=user, text=text)
