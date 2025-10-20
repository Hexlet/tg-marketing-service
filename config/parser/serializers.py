from rest_framework import serializers
from .models import TelegramChannel, Category, Country, Language


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'code')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name',)


class TelegramChannelSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    country_code = serializers.CharField(source='country.code', read_only=True)

    class Meta:
        model = TelegramChannel
        fields = (
            'id',
            'title',
            'subscribers_count',
            'category',
            'is_verified',
            'country_code',
            'photo_url',
        )

    def to_representation(self, instance):
        """Переименовываем поля для соответствия требованиям фронтенда."""
        representation = super().to_representation(instance)
        representation['name'] = representation.pop('title')
        representation['subscribers'] = representation.pop('subscribers_count')
        representation['verified'] = representation.pop('is_verified')
        representation['imageUrl'] = representation.pop('photo_url')
        representation['countryCode'] = representation.pop('country_code')
        return representation


class ChannelRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TelegramChannel, возвращающий данные для рейтинга."""

    class Meta:
        model = TelegramChannel
        fields = (
            'title',
            'photo_url',
            'subscribers_count',
            'avg_post_reach',
        )

    def to_representation(self, instance):
        """Переименовываем поля для удобства фронтенда."""
        representation = super().to_representation(instance)
        representation['channel_name'] = representation.pop('title')
        representation['avatar_url'] = representation.pop('photo_url')
        representation['subscribers'] = representation.pop('subscribers_count')
        representation['avg_views_per_post'] = representation.pop('avg_post_reach')
        return representation