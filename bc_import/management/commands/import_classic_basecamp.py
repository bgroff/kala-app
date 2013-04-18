from bc_import.management.commands._menu import main, MainMenu
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<project_url username password>'
    help = 'Will start a dialog to import your information from classic basecamp.'

    def handle(self, *args, **options):
        if len(args) != 3:
            raise CommandError("The command required 3 arguments: url, username, password. see help for details")
        #main(args[0], args[1], args[2])
        MainMenu()