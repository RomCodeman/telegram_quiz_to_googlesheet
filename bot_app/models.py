from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import User

from bot_app.logger import logger

from bot_app.sheets.sheets_class import UserCredentials


class UserDataDB(models.Model):
    id_db = models.IntegerField(primary_key=True)
    chat_id_db = models.IntegerField()
    login_db = models.CharField(max_length=50)
    name_db = models.CharField(max_length=50)
    phone_num_db = models.CharField(max_length=50)
    answers_db = models.TextField()

    class Meta:
        verbose_name = 'User Data in the DB'
        verbose_name_plural = "User's Data in the DB"

    def __str__(self):
        return f"{self.chat_id_db} | {self.login_db} | {self.answers_db}"

    # Filter records by chat_id_db
    @classmethod
    def filter_chat_id(cls, chat_id):
        return cls.objects.filter(chat_id_db=chat_id)

    @classmethod
    def add_to_db(cls, chat_id, user: UserCredentials, filtered_set: QuerySet):
        user_answers = ", ".join(user.answers)
        chat_id_unique: bool = True
        if filtered_set.exists():  # One or more records
            chat_id_unique = False
            user_data, created = filtered_set.get_or_create(login_db=user.login,
                                                            name_db=user.name,
                                                            phone_num_db=user.phone_num,
                                                            answers_db=user_answers,
                                                            defaults={"chat_id_db": chat_id,
                                                                      "login_db": user.login,
                                                                      "name_db": user.name,
                                                                      "phone_num_db": user.phone_num,
                                                                      "answers_db": user_answers})
            return user_data, created, chat_id_unique
        else:
            try:
                user_data = cls.objects.create(chat_id_db=chat_id, login_db=user.login, name_db=user.name,
                                               phone_num_db=user.phone_num, answers_db=user_answers)
                created = True

                return user_data, created, chat_id_unique
            except Exception as e:
                logger.error(f"New record creating was not successful. Exception: {e}")