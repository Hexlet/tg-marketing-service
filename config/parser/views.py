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
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import F

from config.parser.forms import ChannelParseForm
from config.parser.models import TelegramChannel, Category, Country, Language
from config.parser.parser import tg_parser
from .serializers import TelegramChannelSerializer

log = logging.getLogger(__name__)


class ChannelSearchView(ListAPIView):
    """
    API view для поиска и фильтрации каналов.
    """
    serializer_class = TelegramChannelSerializer

    def get_queryset(self):
        """
        Фильтрует каналы по поисковому запросу 'q' и другим параметрам в URL.
        """
        queryset = TelegramChannel.objects.all()
        
        # Полнотекстовый поиск
        query_param = self.request.query_params.get('q', None)
        if query_param:
            # В реальном приложении этот update должен происходить в фоновой задаче
            TelegramChannel.objects.update(search_vector=(SearchVector('title', weight='A') + SearchVector('description', weight='B')))

            query = SearchQuery(query_param, search_type='websearch')
            queryset = queryset.annotate(
                rank=SearchRank(F('search_vector'), query)
            ).filter(search_vector=query).order_by('-rank')

        # Фильтры по ID (справочники)
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        country_id = self.request.query_params.get('country', None)
        if country_id:
            queryset = queryset.filter(country_id=country_id)

        language_id = self.request.query_params.get('language', None)
        if language_id:
            queryset = queryset.filter(language_id=language_id)

        # Фильтры по булевым флагам
        boolean_filters = {
            'is_verified': 'verified',
            'is_rkn_registered': 'rkn',
            'has_stories': 'stories',
            'has_red_label': 'no_red_label', # инвертированная логика
            'is_scam': 'no_scam', # инвертированная логика
            'is_dead': 'hide_dead' # инвертированная логика
        }

        for db_field, url_param in boolean_filters.items():
            param_value = self.request.query_params.get(url_param, None)
            if param_value is not None:
                # Преобразуем 'true'/'false' из URL в булево значение
                is_true = param_value.lower() in ('true', '1')
                
                # Для некоторых фильтров логика инвертирована (например, no_scam=true означает is_scam=false)
                if url_param in ['no_red_label', 'no_scam', 'hide_dead']:
                    queryset = queryset.filter(**{db_field: not is_true})
                else:
                    queryset = queryset.filter(**{db_field: is_true})

        # Сортировка по умолчанию, если не было поиска
        if not query_param:
            queryset = queryset.order_by('-subscribers_count')
            
        return queryset


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