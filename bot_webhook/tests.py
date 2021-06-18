from django.test import TestCase
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User, Bot
from .serializers import UserSerializer


class MyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        Bot.set_token('newtoken')

        self.integrated_user = User.objects.create(
            name='Fulano de Tal', chat_id='983126414', phone_number='5551999999999'
        )

        self.already_integrated = {
            'message': {
                'chat': {
                    'id': 983126414,
                    'first_name': 'Fulano',
                    'last_name': 'de Tal',
                    'type': 'private',
                },
            },
        }

        self.start_integration = {
            'message': {
                'chat': {
                    'id': 4564654654,
                    'first_name': 'Ciclano',
                    'last_name': 'de Tal',
                    'type': 'private',
                },
                'text': '/start',
            },
        }

        self.complete_integration = {
            'message': {
                'chat': {
                    'id': 4564654654,
                    'first_name': 'Ciclano',
                    'last_name': 'de Tal',
                    'type': 'private',
                },
                'contact': {'phone_number': '5551999999999'},
            },
        }

        self.data_users = [
            {'name': 'João da Silva', 'chat_id': '4554654654', 'phone_number': '5511888888888'},
            {'name': 'Pedro Pedroso', 'chat_id': '5456465464', 'phone_number': '5511777777777'},
            {'name': 'Silvio Silveira', 'chat_id': '4478787878', 'phone_number': '5551999999999'},
        ]

        self.message_without_text = {'name': self.integrated_user.name}

        self.message_without_user_info = {'text': 'mensagem sem user info'}

        self.valid_message = {
            'phone_number': self.integrated_user.phone_number,
            'text': 'uma mensagem válida',
        }


class TestViews(MyTestCase):
    def test_should_not_create_user_if_user_is_already_integrated(self):
        User.objects.create(name='Fulano de Tal', chat_id='983126414', phone_number='5551999999999')
        response = self.client.post(reverse('event'), self.already_integrated, format='json')
        self.assertEqual(json.loads(response.content), {'message': 'Você já está integrado!'})

    def test_should_start_integration_if_text_in_message_and_user_does_not_exist(self):
        response = self.client.post(reverse('event'), self.start_integration, format='json')
        self.assertEqual(json.loads(response.content), {'message': 'Integração iniciada.'})

    def test_should_complete_integration_and_create_user_if_contact_in_message_and_user_does_not_exist(self):
        user_count = User.objects.count()
        response = self.client.post(reverse('event'), self.complete_integration, format='json')
        self.assertEqual(json.loads(response.content), {'message': 'Integração concluída.'})
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_api_users_should_get_all_users(self):
        for user in self.data_users:
            User.objects.create(name=user['name'], chat_id=user['chat_id'], phone_number=user['phone_number'])
        response = self.client.get(reverse('users'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(json.loads(json.dumps(response.data)), serializer.data)

    def test_api_messages_should_not_create_or_send_message_if_payload_does_not_have_user_at_least_one_user_info(self):
        response = self.client.post(reverse('messages'), self.message_without_user_info, format='json')
        self.assertEqual(
            json.loads(response.content), {'erro': 'Por favor, forneça alguma informação válida do destinário.'}
        )

    def test_api_messages_should_not_create_or_send_message_if_payload_does_not_have_text(self):
        response = self.client.post(reverse('messages'), self.message_without_text, format='json')
        self.assertEqual(json.loads(response.content), {'erro': 'Campo text obrigatório.'})

    def test_api_messages_should_create_and_send_messages_to_user_if_message_is_valid(self):
        response = self.client.post(reverse('messages'), self.valid_message, format='json')
        self.assertEqual(json.loads(response.content), {'sucesso': 'A mensagem foi enviada com sucesso!'})
