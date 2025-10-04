import logging

from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib import messages

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView
from rest_framework.generics import ListAPIView
from telethon import TelegramClient
from telethon.sessions import StringSession

from config.parser.forms import ChannelParseForm
from config.parser.models import TelegramChannel, Category, Country, Language
from config.parser.parser import tg_parser
from .serializers import TelegramChannelSerializer

log = logging.getLogger(__name__)


class ChannelSearchView(ListAPIView):
    """
    API view для поиска и фильтрации каналов.
    Пока что просто возвращает все каналы.
    """
    queryset = TelegramChannel.objects.all().order_by('-subscribers_count')
    serializer_class = TelegramChannelSerializer


class ParserView(FormView):
    form_class = ChannelParseForm
    template_name = 'parser/parse_channel.html'
    success_url = reverse_lazy("parser:list")

    def get_telegram_client(self):
        """Get Telegram client for parser work"""
        return TelegramClient(
            StringSession(settings.TELEGRAM_SESSION_STRING),
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH,
        )

    async def async_tg_parser(self, url, limit=10):
        """Parser wrapper"""
        client = self.get_telegram_client()
        await client.connect()
        try:
            return await tg_parser(url, client, limit)
        finally:
            await client.disconnect()

    def save_channel(self, data):
        """Create or update channel"""
        # Преобразуем строковые данные в объекты моделей
        category_obj, _ = Category.objects.get_or_create(name=data.get('category', 'Без категории'))
        country_obj, _ = Country.objects.get_or_create(name=data.get('country', 'Неизвестно'), defaults={'code': 'XX'})
        language_obj, _ = Language.objects.get_or_create(name=data.get('language', 'Неизвестно'))

        channel, created = TelegramChannel.objects.update_or_create(
            channel_id=data["channel_id"],
            defaults={
                'title': data.get('title'),
                'username': data.get('username'),
                'description': data.get('description'),
                'subscribers_count': data.get('participants_count', 0),
                'photo_url': data.get('photo_url'),
                # Ниже - примерные данные, их нужно будет получать при парсинге
                'avg_post_reach': data.get('average_views', 0),
                'language': language_obj,
                'country': country_obj,
                'category': category_obj,
                'parsed_at': timezone.now(),
            }
        )

        if created:
            log.info(f"New channel created: {channel.title}")
        else:
            log.info(f"Channel updated: {channel.title}")

        return channel, created

    def form_valid(self, form):
        """ Обработка формы """
        identifier = form.cleaned_data['channel_identifier']
        limit = form.cleaned_data['limit']
        language = form.cleaned_data['language']
        country = form.cleaned_data['country']
        category = form.cleaned_data['category']
        log.info(f'Начинаем обработку данных для канала; '
                 f'- {identifier} лимит - {limit}')
        try:
            # Start async parsing function
            async_parser = async_to_sync(self.async_tg_parser)
            parsed_data = async_parser(identifier, limit)
            parsed_data.update({'language': language.name if language else None,
                                'country': country.name if country else None,
                                'category': category.name if category else None})
            
            log.info(f'Парсинг завершен для канала;'
                     f'- {parsed_data.get("title")} ({parsed_data.get("channel_id")}')

            # Saving data
            channel, created = self.save_channel(parsed_data)

            # Generating user message
            message = (
                f"New channel created: {channel.title}"
                if created
                else f"Channel updated: {channel.title}"
            )
            messages.success(self.request, message)

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class ParserListView(ListView):
    model = TelegramChannel
    template_name = 'parser/channels_list.html'
    context_object_name = "channels"
    ordering = ["-parsed_at"]


class ParserDetailView(DetailView):
    model = TelegramChannel
    template_name = 'parser/channel_detail.html'
    context_object_name = "channel"


# Create your views here.