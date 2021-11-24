from django.contrib import admin
from django.contrib.auth.models import Group

from bot_app.models import UserDataDB

# # Register your models here.
admin.site.site_header = "Telegram Bot"
admin.site.unregister(Group)


@admin.register(UserDataDB)
class UserDataDBAdmin(admin.ModelAdmin):
    list_display = ('chat_id_db', 'id_db', 'login_db', 'name_db', 'phone_num_db', 'answers_db')

    list_filter = ('chat_id_db', 'answers_db')

    fieldsets = (
        ('Common information about chat item', {
            'fields': ('id_db', 'chat_id_db', 'login_db', 'answers_db',)
        }),
        ('Additional information about chat item', {
            'fields': ('name_db', 'phone_num_db',)
        }),
    )