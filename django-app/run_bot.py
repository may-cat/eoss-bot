import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tenants.settings")
django.setup()

from tbot.dispatcher import run_bot

if __name__ == "__main__":
    run_bot()
