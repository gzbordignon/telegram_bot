from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Bot

logger = get_task_logger(__name__)


@shared_task
def send_message(token, chat_id, text, reply_markup=None):
    Bot.send_message(token, chat_id, text, reply_markup)


@shared_task
def create_message(user_id, text):
    Bot.create_message(user_id, text)
