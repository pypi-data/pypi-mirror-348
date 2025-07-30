import os
import shutil
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Create a Django app with a DDD structure"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)

    def handle(self, *args, **kwargs):
        app_name = kwargs["app_name"]
        target_path = os.path.join(os.getcwd(), app_name)
        template_path = os.path.join(os.path.dirname(__file__), "../../../templates/ddd_app")

        if os.path.exists(target_path):
            raise CommandError(f"The folder '{{app_name}}' already exists.")

        shutil.copytree(template_path, target_path)
        self.stdout.write(self.style.SUCCESS(f"App '{{app_name}}' created with DDD structure"))