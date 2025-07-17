import logging

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views.generic import FormView, ListView, DetailView
from django.conf import settings

from asgiref.sync import async_to_sync
from telethon import TelegramClient
from telethon.sessions import StringSession

from config.parser.forms import ChannelParseForm
from config.parser.parser import tg_parser
from config.parser.models import TelegramChannel, ChannelStats


log = logging.getLogger(__name__)


class ParserView(FormView):
    form_class = ChannelParseForm
    template_name = 'parser/parse_channel.html'
    success_url = reverse_lazy('parser:list')

    def get_telegram_client(self):
        """ Получаем клиент телеграма для работы парсера """
        return TelegramClient(
            StringSession(settings.TELEGRAM_SESSION_STRING),
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        )

    async def async_tg_parser(self, url, limit=10):
        """ Обертка для парсера """
        client = self.get_telegram_client()
        await client.connect()
        try:
            return await tg_parser(url, client, limit)
        finally:
            await client.disconnect()

    def save_channel(self, data):
        """Создаем или обновляем канал"""
        channel, created = TelegramChannel.objects.update_or_create(
            channel_id=data['channel_id'],
            defaults={
                'title': data['title'],
                'username': data['username'],
                'description': data['description'],
                'participants_count': data['participants_count'],
                'pinned_messages': data['pinned_messages'],
                'last_messages': data['last_messages'],
                'average_views': data['average_views'],
            }
        )

        if created:
            log.info(f'Создан новый канал: {channel.title}')
        else:
            log.info(f'Обновлен канал: {channel.title}')

        return channel, created

    def save_stats(self, channel, data):
        """Создаем запись статистики с расчетом прироста"""
        last_stats = ChannelStats.objects.filter(channel=channel).order_by('-parsed_at').first()
        current_date = timezone.now()  # Используем timezone.now() вместо datetime.now()
        current_count = data['participants_count']

        if last_stats and last_stats.parsed_at.date() != current_date.date():
            daily_growth = current_count - last_stats.participants_count
        else:
            daily_growth = last_stats.daily_growth if last_stats else 0

        # Создаём новую статистику
        ChannelStats.objects.create(
            channel=channel,
            participants_count=current_count,
            daily_growth=daily_growth,
            parsed_at=current_date
        )

        # Обновляем дату парсинга для телеграм канала
        channel.parsed_at = current_date
        channel.save(update_fields=['parsed_at'])
        log.info(f'Для канала: {channel.title} записана статистика; '
                 f'- Подписчики: {current_count} прирост: {daily_growth}')


    def form_valid(self, form):
        """ Обработка формы """
        identifier = form.cleaned_data['channel_identifier']
        limit = form.cleaned_data['limit']
        log.info(f'Начинаем обработку данных для канала; '
                 f'- {identifier} лимит - {limit}')

        try:
            # Запуск асинхронной функции парсинга
            async_parser = async_to_sync(self.async_tg_parser)
            parsed_data = async_parser(identifier, limit)
            log.info(f'Парсинг завершен для канала;'
                     f'- {parsed_data['title']} ({parsed_data['channel_id']}')

            # Сохранение полученных данных
            channel, created = self.save_channel(parsed_data)
            self.save_stats(channel, parsed_data)

            # Составление сообщения для пользователя
            message = f'Новый канал добавлен: {channel.title}' \
                if created \
                else f'Канал обновлен: {channel.title}'
            messages.success(self.request, message)

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class ParserListView(ListView):
    model = TelegramChannel
    template_name = 'parser/channels_list.html'
    context_object_name = 'channels'
    ordering = ['-parsed_at']


class ParserDetailView(DetailView):
    model = TelegramChannel
    template_name = 'parser/channel_detail.html'
    context_object_name = 'channel'
# Create your views here.