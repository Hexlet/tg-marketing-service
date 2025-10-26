import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Создает строку сессии телеграм для пользователя'

    def handle(self, *args, **options):
        self.stdout.write("Начинаем процесс создания сессии...")

        api_id = os.getenv('TELEGRAM_API_ID')
        api_hash = os.getenv('TELEGRAM_API_HASH')
        phone = os.getenv('PHONE')

        if not all([api_id, api_hash, phone]):
            self.stdout.write(self.style.ERROR(
                "Переменные TELEGRAM_API_ID, TELEGRAM_API_HASH и PHONE должны быть установлены в .env файле."
            ))
            return

        async def main():
            client = TelegramClient(
                StringSession(),
                int(api_id),
                api_hash
            )
            await client.start(phone=phone)

            session_string = client.session.save()
            self.stdout.write(self.style.SUCCESS(
                "\nСессия успешно создана! Вот ваша строка сессии:"
            ))
            self.stdout.write(f"\n{session_string}\n")
            self.stdout.write(self.style.WARNING(
                "Скопируйте эту строку и вставьте в ваш .env файл как значение для TELEGRAM_SESSION_STRING"
            ))

            await client.disconnect()

        # Запускаем асинхронную функцию
        asyncio.run(main())
