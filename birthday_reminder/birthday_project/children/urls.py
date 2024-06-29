from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import-children/', views.import_children, name='import_children'),
    path('send-birthday-messages/', views.send_birthday_messages, name='send_birthday_messages'),
    path('notify-upcoming-birthdays/', views.notify_upcoming_birthdays, name='notify_upcoming_birthdays'),
]
