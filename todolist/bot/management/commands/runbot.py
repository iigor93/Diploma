import random
import string
from datetime import datetime

import redis

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from bot.tg.client import TgClient
from bot.models import TgUser

from goals.models import Goal, GoalCategory, BoardParticipant


class Command(BaseCommand):
    help = "Runs Telegram Bot"
    loaddata_command = "runbot"
    redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
    

    def generate_alphanum_random_string(self):
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.sample(letters_and_digits, 4))
        
        for key in self.redis_instance.keys("*"):
            if key == random_string:
                return self.generate_alphanum_random_string()

        return random_string

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient()
        while True:
            try:
                res = tg_client.get_updates(offset=offset)
            except:
                res = None
            if res:
                for item in res.result:
                    offset = item.update_id + 1

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
        
        user_condition = str(current_user.user_tgid) + '_condition'
        user_category = str(current_user.user_tgid) + '_category'
        
        current_condition = self.redis_instance.get(user_condition)
        if current_condition is None or current_condition == 'Nil':
            if text == '/goal':
                goals = Goal.objects.select_related('category__board', 'user').filter(
                    category__board__participants__user=current_user.user, is_deleted=False)
                if goals:
                    return_text = ''
                    for goal in goals:
                        return_text += (goal.title + '\r\n')
                    return return_text

                return 'No goals found'

            if text == '/create':

                categories = GoalCategory.objects.select_related('board', 'user').filter(
                    (Q(board__participants__role=BoardParticipant.Role.OWNER) | Q(
                        board__participants__role=BoardParticipant.Role.WRITER)),
                    board__participants__user=current_user.user,
                    is_deleted=False)

                if categories:
                    self.redis_instance.set(user_condition, 'choose_category')
                    return_text = ''
                    for category in categories:
                        return_text += (category.title + '\r\n')
                    return return_text

                return 'No categories found'
        
        if current_condition == 'choose_category':
            if text == '/cancel':
                self.redis_instance.delete(user_condition)
                self.redis_instance.delete(user_category)
                
                return 'canceled'
            else:
                categories = GoalCategory.objects.select_related('board', 'user').filter(
                    (Q(board__participants__role=BoardParticipant.Role.OWNER) | Q(
                        board__participants__role=BoardParticipant.Role.WRITER)),
                    board__participants__user=current_user.user,
                    is_deleted=False)

                for cat in categories:
                    if text == cat.title:
                        self.redis_instance.set(user_condition, 'goal_create')
                        self.redis_instance.set(user_category, cat.id)
                        
                        return 'Enter goal title'

                return 'Wrong input'

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
