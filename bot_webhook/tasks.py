from celery import shared_task
from .models import User


@shared_task
def create_user(name=None, chat_id=None, phone_number=None):
    User.objects.create(name=name, chat_id=chat_id, phone_number=phone_number)

def find_user(payload):
    filters = ['name', 'chat_id', 'phone_number']
    for filter in filters:
        user = User.objects.filter(**{filter: payload[filter]}).first()
        if user is not None:
            break
    return user