import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()


from aiogram.utils import executor
from core.bot import dp


if __name__ == "__main__":
    executor.start_polling(dp)