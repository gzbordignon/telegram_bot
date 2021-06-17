from celery import shared_task
from .models import Message, User
import requests
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def send_message(token, chat_id, text, reply_markup=None):
    url = 'https://api.telegram.org/bot' + token + '/sendMessage'
    data = dict(chat_id=chat_id, text=text, reply_markup=reply_markup)
    requests.post(url, data)


@shared_task
def create_message(user_id, text):
    logger.info(text)
    user = User.objects.get(pk=user_id)
    Message.objects.create(sent_to=user, text=text)
