# django_ddd_template/cli.py
from django_ddd_template.management.commands.startapp_ddd import Command

def main():
    command = Command()
    command.handle()
