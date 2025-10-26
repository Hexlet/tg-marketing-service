from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from config.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название страны')
    code = models.CharField(max_length=2, unique=True, verbose_name='Код страны (ISO 3166-1 alpha-2)')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Язык')

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return self.name


class TelegramChannel(models.Model):
    # Основная информация
    channel_id = models.BigIntegerField(unique=True, verbose_name='ID канала')
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Username')
    title = models.CharField(max_length=255, verbose_name='Название канала')
    description = models.TextField(blank=True, null=True, verbose_name='Описание канала')
    photo_url = models.URLField(max_length=2048, blank=True, null=True, verbose_name='Аватар')
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата создания')

    # Справочники
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Страна')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Язык')

    # Статистика
    subscribers_count = models.IntegerField(default=0, verbose_name='Подписчики')
    avg_post_reach = models.IntegerField(default=0, verbose_name='Средний охват поста')
    avg_post_reach_24h = models.IntegerField(default=0, verbose_name='Средний охват поста (24ч)')
    err = models.FloatField(default=0.0, verbose_name='ERR')
    er = models.FloatField(default=0.0, verbose_name='ER')
    male_audience_percentage = models.FloatField(default=0.0, verbose_name='Мужская аудитория (%)')
    female_audience_percentage = models.FloatField(default=0.0, verbose_name='Женская аудитория (%)')

    # Флаги
    is_verified = models.BooleanField(default=False, verbose_name='Верифицирован')
    is_rkn_registered = models.BooleanField(default=False, verbose_name='Зарегистрирован в РКН')
    has_stories = models.BooleanField(default=False, verbose_name='Есть сторис')
    has_red_label = models.BooleanField(default=False, verbose_name='Красная метка')
    is_scam = models.BooleanField(default=False, verbose_name='SCAM/FAKE')
    is_dead = models.BooleanField(default=False, verbose_name='"Мертвый"')

    # Технические поля
    parsed_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего парсинга')
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        verbose_name = 'Telegram канал'
        verbose_name_plural = 'Telegram каналы'
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['subscribers_count']),
            models.Index(fields=['avg_post_reach']),
            models.Index(fields=['err']),
        ]

    def __str__(self):
        return self.title
