from django.core.management.base import BaseCommand
#from authenticator.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with additional fields'

    def handle(self, *args, **options):
        mobile_number = input("Enter mobile number: ")
        email = input("Enter email address: ")
        password = input("Enter password: ")

        try:
            user = User.objects.create_superuser(mobile_number=mobile_number, email=email, password=password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating superuser: {e}'))
