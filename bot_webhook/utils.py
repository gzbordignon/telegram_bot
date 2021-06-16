import requests


def send_message(chat_id, text, reply_markup=None):
    url = 'https://api.telegram.org/bot1175594888:AAFM9ACsHYs5muY3Vs212V_ahc1HCQVFi6c/sendMessage'
    data = dict(chat_id=chat_id, text=text, reply_markup=reply_markup)
    requests.post(url, data)
