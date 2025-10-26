from django.contrib import admin
from .models import TelegramChannel, Category, Country, Language


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'subscribers_count', 'category', 'country', 'language', 'is_verified', 'parsed_at')
    list_filter = ('is_verified', 'is_scam', 'is_dead', 'category', 'country', 'language', 'parsed_at')
    search_fields = ('title', 'username', 'description')
    readonly_fields = ('parsed_at',)
    ordering = ('-subscribers_count',)
    list_per_page = 25

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'username', 'description', 'photo_url', 'channel_id', 'creation_date')
        }),
        ('Классификация', {
            'fields': ('category', 'country', 'language')
        }),
        ('Статистика', {
            'fields': ('subscribers_count', 'avg_post_reach', 'avg_post_reach_24h', 'err', 'er', 'male_audience_percentage', 'female_audience_percentage')
        }),
        ('Флаги', {
            'fields': ('is_verified', 'is_rkn_registered', 'has_stories', 'has_red_label', 'is_scam', 'is_dead'),
            'classes': ('collapse',)
        }),
        ('Техническая информация', {
            'fields': ('parsed_at', 'search_vector'),
            'classes': ('collapse',)
        }),
    )
