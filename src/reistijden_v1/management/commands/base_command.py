from django.core.management import BaseCommand


class MyCommand(BaseCommand):

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def notice(self, msg):
        self.stdout.write(self.style.NOTICE(msg))

    def error(self, msg):
        self.stdout.write(self.style.ERROR(msg))
