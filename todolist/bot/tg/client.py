from bot.tg import dc

from django.conf import settings

import requests


class TgClient:
    """Класс для приема и отправки сообщений в Телеграмм"""
    SEND_MESSAGE_METHOD: str = 'sendMessage'

    def __init__(self):
        self.token = settings.TG_BOT_TOKEN

    def get_url(self, method: str = ''):
        return "https://api.telegram.org/bot%s/%s" % (self.token, method)  
        
    def get_updates(self, offset: int = 0, timeout: int = 60): 
        
        method = 'getUpdates?offset=%d&timeout=%d' % (offset, timeout)
        url = self.get_url(method=method)
        
        tg_response = requests.get(url)
        data = tg_response.json()
        for item in data['result']:
            item['message']['from_'] = item['message'].pop('from')
    
        return dc.GetUpdatesResponseSchema.load(data)
        
    def send_message(self, chat_id: int, text: str): 
        url = self.get_url(method=self.SEND_MESSAGE_METHOD)
        message = {'chat_id': chat_id, 'text': text}
        tg_response = requests.post(url, json=message)
        data = tg_response.json()
        
        data['result']['from_'] = data['result'].pop('from')
            
        return dc.SendMessageResponseSchema.load(data)
