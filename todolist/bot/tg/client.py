import requests

from django.conf import settings
from bot.tg import dc


class TgClient:
    def __init__(self):
        self.token = settings.TG_BOT_TOKEN

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> dc.GetUpdatesResponseSchema:
        method = f'getUpdates?offset={offset}&timeout={timeout}'
        url = self.get_url(method=method)
        
        tg_response = requests.get(url)
        data = tg_response.json()
        for item in data['result']:
            item['message']['from_'] = item['message'].pop('from')
    
        return dc.GetUpdatesResponseSchema.load(data)
        
    def send_message(self, chat_id: int, text: str) -> dc.SendMessageResponseSchema:
        method = f'sendMessage'
        url = self.get_url(method=method)
        message = {'chat_id': chat_id, 'text': text}
        tg_response = requests.post(url, json=message)
        data = tg_response.json()
        
        data['result']['from_'] = data['result'].pop('from')
            
        return dc.SendMessageResponseSchema.load(data)
