# Teleint

## Modo de uso

Rode o docker container
```
$ docker-compose up -d
```

Rode as migrações
```
$ docker-compose exec web python manage.py migrate
```

Rode o Ngrok:
```
./ngrok http 8000
```

Set webhook enviando um JSON contendo a url https do Ngrok para o seguinte endereço:

    localhost:8000/set_webhook/
    
    request
    JSON exemplo:
    {
      "ngrok_url": "https://e10cb065222e.ngrok.io",
      "token": seu_bot_token # opcional, se não enviar um token será usado um bot padrão
    }
    
    response
    {
      "message": "Webhook was set"
    }
    
    
Faça a integração:

    Dê um comando /start no bot e após a resposta compartilhe seu contato


## API

### GET /users/
 
    response
    {
      "id": 1,
      "nome": "Fulano de Tal",
      "chat_id": "123456789",
      "phone_number": "5551999999999"
    }
    
### POST /messages/ - mensagem a ser enviada para o telegram do usuário
    
    O payload deve conter um dos seguintes atributos nome/chat_id/phone_number e obrigatoriamente o text
    
    request
    JSON exemplo:
    {
      "nome": "Fulano de Tal",
      "text": "Mensagem a ser enviada"
    }
    
    response
    {
      "message": "A mensagem foi enviada com sucesso!"
    }
    



