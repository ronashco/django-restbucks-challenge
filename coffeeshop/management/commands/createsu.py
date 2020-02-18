from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin")
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
        if not User.objects.filter(username="alireza").exists():
            User.objects.create_user("alireza")
            self.stdout.write(self.style.SUCCESS('Successfully created new user'))
