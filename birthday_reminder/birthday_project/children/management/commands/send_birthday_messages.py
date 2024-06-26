from django.core.management.base import BaseCommand
from children.models import Child
from datetime import datetime
from twilio.rest import Client

class Command(BaseCommand):
    help = 'Send birthday messages to children'

    def handle(self, *args, **kwargs):
        today = datetime.today().date()
        children = Child.objects.filter(date_of_birth__month=today.month, date_of_birth__day=today.day)

        if children:
            # Twilio credentials
            account_sid = 'your_account_sid'
            auth_token = 'your_auth_token'
            client = Client(account_sid, auth_token)

            for child in children:
                message = f"Happy Birthday, {child.name}!"
                client.messages.create(
                    body=message,
                    from_='+your_twilio_number',
                    to=child.phone_number
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully sent birthday message to {child.name}'))
        else:
            self.stdout.write('No birthdays today.')
