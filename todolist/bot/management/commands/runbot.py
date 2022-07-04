import random
import string
from datetime import datetime

from bot.models import TgUser
from bot.tg.client import TgClient

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from goals.models import BoardParticipant, Goal, GoalCategory

import redis


class Command(BaseCommand):
    help = "Runs Telegram Bot"
    loaddata_command = "runbot"
    redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
    
    OFFSET = 0

    def generate_alphanum_random_string(self):
        """Генерация случайной строки"""
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.sample(letters_and_digits, 4))
        
        for key in self.redis_instance.keys("*"):
            if key == random_string:
                return self.generate_alphanum_random_string()

        return random_string

    def handle(self, *args, **options):
        
        tg_client = TgClient()
        while True:
            try:
                res = tg_client.get_updates(offset=self.OFFSET)
                if res:
                    self.not_verified_user(res, tg_client)
            except:  # noqa E722
                continue
    
    def not_verified_user(self, res, tg_client):
        for item in res.result:
            self.OFFSET = item.update_id + 1
            current_user = self.is_user_exist(item.message.from_.id)
            
            if current_user:
                if current_user.user_id is None:
                    verification_code = self.generate_alphanum_random_string()
                    text = 'Confirm your account \r\n' + verification_code
                            
                    self.redis_instance.set(verification_code, str(current_user.user_tgid), ex=600)
                            
                else:
                    text = self.user_commands(item.message.text, current_user)
                tg_client.send_message(chat_id=item.message.chat.id, text=text)
            else:
                verification_code = self.generate_alphanum_random_string()
                text = 'Hello new User\r\n' + verification_code
                new_user = TgUser.objects.create(
                    user_tgid=item.message.from_.id,
                    chat_tgid=item.message.chat.id)
                        
                self.redis_instance.set(verification_code, str(new_user.user_tgid), ex=600)

                tg_client.send_message(chat_id=item.message.chat.id, text=text)

    def is_user_exist(self, tg_userid):
        try:
            return TgUser.objects.filter(user_tgid__icontains=tg_userid).get()
        except ObjectDoesNotExist:
            return None

    def user_commands(self, text, current_user):
        """Комманды пользователя"""
        user_condition = str(current_user.user_tgid) + '_condition'
        user_category = str(current_user.user_tgid) + '_category'
        
        current_condition = self.redis_instance.get(user_condition)
        
        if current_condition is None or current_condition == 'nil':
            if text == '/goal':
                return self.text_is_goal(current_user)

            if text == '/create':
                return self.text_is_create(current_user, user_condition)

        if current_condition == 'choose_category':
            if text == '/cancel':
                return self.text_is_cancel(user_condition, user_category)
            else:
                return self.text_is_category_name(text, current_user, user_condition, user_category)

        if current_condition == 'goal_create':
            goal_category = self.redis_instance.get(user_category)
            self.redis_instance.delete(user_condition)
            self.redis_instance.delete(user_category)
            
            if text == '/cancel' or text is None:
                return 'canceled'
            Goal.objects.create(title=text,
                                description=text,
                                due_date=datetime.now(),
                                user=current_user.user,
                                category_id=int(goal_category))
            return 'Goal created'
        return 'unknown command'

    def text_is_goal(self, current_user):
        goals = Goal.objects.select_related('category__board', 'user').\
            filter(category__board__participants__user=current_user.user, is_deleted=False)
        if goals:
            return_text = ''
            for goal in goals:
                return_text += (goal.title + '\r\n')
            return return_text

        return 'No goals found'
        
    def text_is_create(self, current_user, user_condition):
        categories = GoalCategory.objects.select_related('board', 'user').\
            filter(board__participants__role__in=(BoardParticipant.Role.OWNER, BoardParticipant.Role.WRITER),
                   board__participants__user=current_user.user,
                   is_deleted=False)

        if categories:
            self.redis_instance.set(user_condition, 'choose_category', ex=600)
            return_text = ''
            for category in categories:
                return_text += (category.title + '\r\n')
            return return_text

        return 'No categories found'

    def text_is_cancel(self, user_condition, user_category):
        self.redis_instance.delete(user_condition)
        self.redis_instance.delete(user_category)
                
        return 'canceled'

    def text_is_category_name(self, text, current_user, user_condition, user_category):
        categories = GoalCategory.objects.select_related('board', 'user').\
            filter(board__participants__role__in=(BoardParticipant.Role.OWNER, BoardParticipant.Role.WRITER),
                   board__participants__user=current_user.user,
                   is_deleted=False)

        for cat in categories:
            if text == cat.title:
                self.redis_instance.set(user_condition, 'goal_create', ex=600)
                self.redis_instance.set(user_category, cat.id, ex=600)
                        
                return 'Enter goal title'

        return 'Wrong input'
