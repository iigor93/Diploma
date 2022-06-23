import random
import string

from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from bot.tg.client import TgClient
from bot.models import TgUser

from goals.models import Goal, GoalCategory, BoardParticipant


class Command(BaseCommand):
    help = "Runs Telegram Bot"

    loaddata_command = "runbot"


    def generate_alphanum_random_string(self):
        letters_and_digits = string.ascii_letters + string.digits
        
        return ''.join(random.sample(letters_and_digits, 4))


    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient()
        while True:
            res = tg_client.get_updates(offset=offset)
            if res:
                for item in res.result:
                    offset = item.update_id + 1
                    
                    current_user = self.is_user_exist(item.message.from_.id)
                    
                    if current_user:
                        if current_user.user_id is None:
                            verification_code = self.generate_alphanum_random_string()
                            text = 'Confirm your account \r\n' + verification_code
                            current_user.verification_code = verification_code
                            current_user.save()
                        else:
                            text = self.user_commands(item.message.text, current_user)
                        tg_client.send_message(chat_id=item.message.chat.id, text=text)
                    else:
                        verification_code = self.generate_alphanum_random_string()
                        text = 'Hello new User\r\n' + verification_code 
                        new_user = TgUser.objects.create(
                            verification_code=verification_code,
                            user_tgid=item.message.from_.id,
                            chat_tgid=item.message.chat.id)
                            
                        tg_client.send_message(chat_id=item.message.chat.id, text=text)

    def is_user_exist(self, tg_userid):
        try:
            return TgUser.objects.filter(user_tgid__icontains=tg_userid).get()
        except ObjectDoesNotExist:
            return None
            
    def user_commands(self, text, current_user):
        if current_user.condition == TgUser.Conditions.BEGIN:
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
                    (Q(board__participants__role=BoardParticipant.Role.OWNER) | Q(board__participants__role=BoardParticipant.Role.WRITER)),
                    board__participants__user=current_user.user, 
                    is_deleted=False)
                
                if categories:
                    current_user.condition = TgUser.Conditions.CHOOSE_CATEGORY
                    current_user.save()
                    return_text = ''
                    for category in categories:
                        return_text += (category.title + '\r\n')
                    return return_text
                
                return 'No categories found'
        
        if current_user.condition == TgUser.Conditions.CHOOSE_CATEGORY:
            if text == '/cancel':
                current_user.condition = TgUser.Conditions.BEGIN
                current_user.save()
                
                return 'canceled'
            else:
                categories = GoalCategory.objects.select_related('board', 'user').filter(
                    (Q(board__participants__role=BoardParticipant.Role.OWNER) | Q(board__participants__role=BoardParticipant.Role.WRITER)),
                    board__participants__user=current_user.user, 
                    is_deleted=False)
                    
                for cat in categories:
                    if text == cat.title:
                        current_user.condition = TgUser.Conditions.GOAL_CREATE
                        current_user.category = cat
                        current_user.save()
                        return 'Enter goal title'
                    
                return 'Wrong input'
        
        if current_user.condition == TgUser.Conditions.GOAL_CREATE:
            current_user.condition = TgUser.Conditions.BEGIN
            current_user.save()
            if text == '/cancel' or text is None:
                return 'canceled'
            Goal.objects.create(title=text, 
                description=text,
                due_date=datetime.now(),
                user=current_user.user, 
                category=current_user.category)
            return 'Goal created'
            
        return 'unknown command'
        
            



            
