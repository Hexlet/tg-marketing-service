import logging

from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View
from inertia import render
from telethon import TelegramClient
from telethon.sessions import StringSession
from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank
)
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from config.parser.forms import ChannelParseForm
from config.parser.models import TelegramChannel, Category, Country, Language
from config.parser.parser import tg_parser
from .serializers import ChannelRatingSerializer

log = logging.getLogger(__name__)


class ChannelRatingView(generics.ListAPIView):
    """
    API-представление для получения рейтинга Telegram-каналов.

    Предоставляет возможность фильтрации по 'category' и 'country',
    а также сортировку по 'subscribers_count' и 'avg_post_reach'.
    """
    queryset = TelegramChannel.objects.all()
    serializer_class = ChannelRatingSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'country']
    ordering_fields = ['subscribers_count', 'avg_post_reach']


class ChannelSearchView(View):
    """
    View для поиска и фильтрации каналов с использованием Inertia.
    """
    def get(self, request, *args, **kwargs):
        queryset = TelegramChannel.objects.all()
        query_param = self.request.GET.get('q', None)

        if query_param:
            # Обновление search_vector для поиска
            TelegramChannel.objects.update(
                search_vector=(
                    SearchVector('title', weight='A') +
                    SearchVector('description', weight='B')
                )
            )

            query = SearchQuery(query_param, search_type='websearch')
            queryset = queryset.annotate(
                rank=SearchRank(F('search_vector'), query)
            ).filter(search_vector=query).order_by('-rank')

        # Фильтры по ID (справочники)
        category_id = self.request.GET.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        country_id = self.request.GET.get('country', None)
        if country_id:
            queryset = queryset.filter(country_id=country_id)

        language_id = self.request.GET.get('language', None)
        if language_id:
            queryset = queryset.filter(language_id=language_id)

        # Фильтры по булевым флагам
        boolean_filters = {
            'is_verified': 'verified',
            'is_rkn_registered': 'rkn',
            'has_stories': 'stories',
            'has_red_label': 'no_red_label',
            'is_scam': 'no_scam',
            'is_dead': 'hide_dead'
        }

        for db_field, url_param in boolean_filters.items():
            param_value = self.request.GET.get(url_param, None)
            if param_value is not None:
                is_true = param_value.lower() in ('true', '1')
                if url_param in ['no_red_label', 'no_scam', 'hide_dead']:
                    queryset = queryset.filter(**{db_field: not is_true})
                else:
                    queryset = queryset.filter(**{db_field: is_true})

        # Фильтры по числовым диапазонам
        range_filters = {
            'subscribers_count': ('subscribers_min', 'subscribers_max'),
            'avg_post_reach': ('reach_min', 'reach_max'),
            'avg_post_reach_24h': ('reach_24h_min', 'reach_24h_max'),
            'err': ('err_min', 'err_max'),
            'er': ('er_min', 'er_max'),
            'male_audience_percentage': (
                'male_audience_min', 'male_audience_max'
            ),
            'female_audience_percentage': (
                'female_audience_min', 'female_audience_max'
            ),
        }

        for db_field, url_params in range_filters.items():
            min_param, max_param = url_params
            min_value = self.request.GET.get(min_param, None)
            max_value = self.request.GET.get(max_param, None)

            if min_value is not None:
                queryset = queryset.filter(**{f'{db_field}__gte': min_value})
            if max_value is not None:
                queryset = queryset.filter(**{f'{db_field}__lte': max_value})

        # Сортировка по умолчанию
        if not query_param:
            queryset = queryset.order_by('-subscribers_count')

        # Формируем props для Inertia
        channels_props = queryset.values(
            'id',
            'title',
            'subscribers_count',
            'is_verified',
            'photo_url',
            category_name=F('category__name'),
            country_code=F('country__code')
        )

        # Переименовываем поля для фронтенда
        channels_list = [
            {
                'id': ch['id'],
                'name': ch['title'],
                'subscribers': ch['subscribers_count'],
                'category': ch['category_name'],
                'verified': ch['is_verified'],
                'countryCode': ch['country_code'],
                'imageUrl': ch['photo_url']
            } for ch in channels_props
        ]

        return render(
            request,
            'Channels/SearchPage',  # Имя React-компонента
            {
                'channels': channels_list,
                'filters': request.GET.dict()
            }
        )


class ParserView(View):
    """
    {
        "component": "Channels/ParsePage",
        "props": {
            "categories": [("news", "Новости и СМИ"), ...],
            "form_errors": {"channel_identifier": ["This field is required."]}
        },
        "url": "/parser/parse/"
    }
    """
    form_class = ChannelParseForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request,
            'Channels/ParsePage',
            {
                'categories': form.fields['category'].choices,
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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
        # For now we get names, but we should probably move to FKs in the form
        category_name = form.cleaned_data['category']
        country_name = form.cleaned_data['country']
        language_name = form.cleaned_data['language']

        log.info(
            f'Начинаем обработку данных для канала; - {identifier} лимит - {limit}'
        )
        try:
            # Start async parsing function
            async_parser = async_to_sync(self.async_tg_parser)
            parsed_data = async_parser(identifier, limit)

            # Here we need to get or create related objects
            category, _ = Category.objects.get_or_create(name=category_name)
            country, _ = Country.objects.get_or_create(
                name=country_name,
                defaults={'code': country_name[:2].upper()}
            )
            language, _ = Language.objects.get_or_create(name=language_name)

            parsed_data.update({'language': language,
                                'country': country,
                                'category': category})

            log.info(
                f'Парсинг завершен для канала; - {parsed_data.get("title")} '
                f'({parsed_data.get("channel_id")}'
            )

            # Saving data
            channel, created = self.save_channel(parsed_data)

            # Generating user message
            message = (
                f"New channel created: {channel.title}"
                if created
                else f"Channel updated: {channel.title}"
            )
            messages.success(self.request, message)

            return HttpResponseRedirect(self.get_success_url())

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Rerender form with errors for Inertia"""
        return render(
            self.request,
            'Channels/ParsePage',
            {
                'categories': form.fields['category'].choices,
                'form_errors': form.errors.get_json_data()
            }
        )

    def get_success_url(self):
        return reverse_lazy("parser:list")


class ParserListView(View):
    """
    {
        "component": "Channels/ListPage",
        "props": {
            "channels": [
                {
                    "id": 1,
                    "name": "Example Channel",
                    "subscribers": 1000,
                    "parsed_at": "2025-10-09T12:00:00Z",
                    "detail_url": "/parser/channel/1/"
                }
            ]
        },
        "url": "/parser/list/"
    }
    """
    def get(self, request, *args, **kwargs):
        channels = TelegramChannel.objects.order_by("-parsed_at")

        channels_props = [
            {
                'id': channel.id,
                'name': channel.title,
                'subscribers': channel.subscribers_count,
                'parsed_at': channel.parsed_at.isoformat(),
                'detail_url': reverse_lazy(
                    'parser:detail', kwargs={'pk': channel.pk}
                )
            }
            for channel in channels
        ]

        return render(
            request,
            'Channels/ListPage',
            {'channels': channels_props}
        )


class ParserDetailView(View):
    """
    {
        "component": "Channels/DetailPage",
        "props": {
            "channel": {
                "id": 1,
                "name": "Example Channel",
                "username": "example_channel",
                "description": "A description.",
                "subscribers": 1000,
                "photo_url": "http://example.com/photo.jpg",
                "category": "News",
                "country": "Unknown",
                "language": "English",
                "avg_post_reach": 500,
                "err": 50.0,
                "is_verified": true,
                "parsed_at": "2025-10-09T12:00:00Z"
            }
        },
        "url": "/parser/channel/1/"
    }
    """
    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(TelegramChannel, pk=kwargs['pk'])

        channel_props = {
            'id': channel.id,
            'name': channel.title,
            'username': channel.username,
            'description': channel.description,
            'subscribers': channel.subscribers_count,
            'photo_url': channel.photo_url,
            'category': getattr(channel.category, 'name', None),
            'country': getattr(channel.country, 'name', None),
            'language': getattr(channel.language, 'name', None),
            'avg_post_reach': channel.avg_post_reach,
            'err': channel.err,
            'is_verified': channel.is_verified,
            'parsed_at': (
                channel.parsed_at.isoformat() if channel.parsed_at else None
            ),
        }

        return render(
            request,
            'Channels/DetailPage',
            {'channel': channel_props}
        )


# Create your views here.