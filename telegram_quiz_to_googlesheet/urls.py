"""telegram_quiz_to_googlesheet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bot_app import views

from django.views.decorators.csrf import csrf_exempt

# curl --header "Content-Type: application/json" --request POST --data "$(cat my_json_file.json)" http://127.0.0.1:8000/hook/

urlpatterns = [
    path('admin/', admin.site.urls),
    # Simplest protection against unwanted webhook using
    path('uaioh13f45iulghd93857sednc/hook/', csrf_exempt(views.BotToSheetView.as_view())),
    path('register/hook/', views.register),

]

