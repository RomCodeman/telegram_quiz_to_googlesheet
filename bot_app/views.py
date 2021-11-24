import json

import telebot
from django.http import HttpResponse, HttpRequest
from django.views import View

from bot_app.bot_app_logic import bot
from bot_app.logger import logger
from config import TOKEN

# https://api.telegram.org/bot<token>/setWebhook?url=<url>/<urlpattern>
# https://api.telegram.org/bot<token>/deleteWebhook?url=<url>/<urlpattern>
url = "https://telebot-to-sheets.herokuapp.com"
link = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}/uaioh13f45iulghd93857sednc/hook/"


def register(request: HttpRequest):
    bot.remove_webhook()
    bot.set_webhook(url=link)
    return HttpResponse("Hook ready")


class BotToSheetView(View):
    # Webhook
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.headers.get('content-type') == 'application/json':
            try:
                json_string = json.dumps(json.loads(request.body))
                update = telebot.types.Update.de_json(json_string)
                bot.process_new_updates([update])  # Transferring updates to the bot module
            except json.decoder.JSONDecodeError as error:
                logger.error(f"{error}")
                return HttpResponse(f"{error}")

            return HttpResponse('OK')
