import json
import requests
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import User, Bot
from .serializers import UserSerializer
from .tasks import send_message, create_message

# https://api.telegram.org/bot1175594888:AAFM9ACsHYs5muY3Vs212V_ahc1HCQVFi6c/getMe
# {'update_id': 756137288,
#     'message': {
#         'message_id': 374,
#         'from': {'id': 983126414, 'is_bot': False, 'first_name': 'Guilherme', 'last_name': 'Bordignon', 'language_code': 'pt-br'},
#         'chat': {'id': 983126414, 'first_name': 'Guilherme', 'last_name': 'Bordignon', 'type': 'private'},
#         'date': 1623727384, 'text': '/start', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]
#     }
# }
# token = '1175594888:AAFM9ACsHYs5muY3Vs212V_ahc1HCQVFi6c'


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'set_webhook': reverse('set_webhook', request=request, format=format),
            'event': reverse('event', request=request, format=format),
            'users': reverse('users', request=request, format=format),
            'messages': reverse('messages', request=request, format=format),
        }
    )


@api_view(['POST'])
def set_webhook(request):
    payload = request.data
    ngrok_url = payload['ngrok_url']
    token = payload['token']
    Bot.set_token(token)
    url = f'https://api.telegram.org/bot{token}/setWebhook?url={ngrok_url}/event/'
    response = requests.get(url)
    response_dict = json.loads(response.text)
    return JsonResponse({'message': response_dict['description']}, status=response.status_code)


@api_view(['POST'])
def event(request):
    data = json.loads(request.body)
    message = data['message']
    chat_id = message['chat']['id']
    first_name = message['chat']['first_name']
    last_name = message['chat']['last_name']
    fullname = first_name + ' ' + last_name
    token = Bot.get_token()
    user = User.objects.filter(chat_id=chat_id).first()
    if user is not None:
        text = f'Olá, {first_name}! Você já está integrado!'
        send_message.delay(token, chat_id, text)
    else:
        # if user sent a message
        if 'text' in message:
            if '/start' in message['text']:
                text = f'Olá, {first_name}! Prazer em conhecer você! Meu nome é Metabee. Compartilhe seu contato para completar a integração.'
                reply_markup = json.dumps(
                    {'keyboard': [[{'text': 'Share contact', 'request_contact': True}]]}
                )
                send_message.delay(token, chat_id, text, reply_markup)
        # if user shared his contact
        elif 'contact' in message:
            phone_number = message['contact']['phone_number']
            User.objects.create(name=fullname, chat_id=chat_id, phone_number=phone_number)
            text = 'Obrigado pela sua integração!'
            send_message.delay(token, chat_id, text)
    return JsonResponse({'message': 'Hello'})


@api_view(['GET'])
def users(request):
    """
    List all users that have accepted integration.
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
    token = Bot.get_token()
    filters = ['name', 'chat_id', 'phone_number']
    if 'text' in payload:
        text = payload['text']
        for filter in filters:
            if filter in payload:
                user = User.objects.filter(**{filter: payload[filter]}).first()
                if user is not None:
                    break
        if user is not None:
            create_message.delay(user.id, text)
            send_message.delay(token, user.chat_id, text)
            return JsonResponse({'message': 'Message was sent successfuly!'})
        else:
            return JsonResponse({'error': "There isn't a user with this credentials."})
    else:
        return JsonResponse({'error': 'The message needs a text.'})
