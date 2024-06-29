import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Child
import datetime
from twilio.rest import Client

def home(request):
    return render(request, 'children/home.html')

def import_children(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                child, created = Child.objects.get_or_create(
                    name=row['name'],
                    date_of_birth=row['date_of_birth'],
                    phone_number=row['number']
                )
                if created:
                    print(f'Successfully added {child.name}')
                else:
                    print(f'{child.name} already exists')
            return HttpResponse("Children imported successfully.")
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')
    return render(request, 'children/import_children.html')

def send_birthday_messages(request):
    today = datetime.date.today()
    children = Child.objects.filter(date_of_birth__month=today.month, date_of_birth__day=today.day)
    for child in children:
        send_birthday_message(child)
    return HttpResponse("Birthday messages sent successfully.")

def notify_upcoming_birthdays(request):
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    upcoming_birthdays = Child.objects.filter(date_of_birth__month=next_week.month, date_of_birth__day=next_week.day)
    if upcoming_birthdays.exists():
        message = "Upcoming birthdays:\n" + "\n".join([f"{child.name} on {child.date_of_birth}" for child in upcoming_birthdays])
        print(message)
    return HttpResponse("Admin notified about upcoming birthdays.")

def send_birthday_message(child):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Happy Birthday, {child.name}!",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=child.phone_number
    )
    print(f'Message sent to {child.name}')
