from bot_webhook.serializers import UserSerializer
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer
from .tasks import create_user, find_user
from .utils import send_message
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# https://api.telegram.org/bot1175594888:AAFM9ACsHYs5muY3Vs212V_ahc1HCQVFi6c/setWebhook?url=https://8458691783d0.ngrok.io/event/
# {'update_id': 756137288,
#     'message': {
#         'message_id': 374,
#         'from': {'id': 983126414, 'is_bot': False, 'first_name': 'Guilherme', 'last_name': 'Bordignon', 'language_code': 'pt-br'},
#         'chat': {'id': 983126414, 'first_name': 'Guilherme', 'last_name': 'Bordignon', 'type': 'private'},
#         'date': 1623727384, 'text': '/start', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]
#     }
# }


@csrf_exempt
def event(request):
    data = json.loads(request.body)
    message = data['message']
    chat_id = message['chat']['id']
    first_name = message['chat']['first_name']
    last_name = message['chat']['last_name']
    fullname = first_name + ' ' + last_name
    user = User.objects.filter(chat_id=chat_id).first()
    if user:
        text = f'Olá, {first_name}! Você já está integrado!'
        send_message(chat_id, text)
    else:
        if 'text' in message:
            if '/start' in message['text']:
                text = f'Olá, {first_name}! Prazer em conhecer você! Meu nome é Metabee. Compartilhe seu contato para completar a integração.'
                reply_markup = json.dumps(
                    {'keyboard': [[{'text': 'Share contact', 'request_contact': True}]]}
                )
                send_message(chat_id, text, reply_markup)
        elif 'contact' in message:
            phone_number = message['contact']['phone_number']
            create_user(name=fullname, chat_id=chat_id, phone_number=phone_number)
            text = 'Obrigado pela sua integração!'
            send_message(chat_id, text)
    return JsonResponse({'message': 'Hello'})


@api_view(['GET'])
def users(request):
    """
    List all users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def messages(request):
    """
    Send message to user
    """
    payload = request.data
    user = find_user(payload)
    send_message(user.chat_id, payload['text'])
    return JsonResponse({'hello': 'hello'})
