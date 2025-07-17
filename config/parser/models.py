from django.db import models


class TelegramChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True, verbose_name='ID канала')
    # invite_link = models.URLField(max_length=255, blank=True, null=True, verbose_name='Инвайт ссылка')
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Username')
    title = models.CharField(max_length=255, verbose_name='Название канала')
    description = models.TextField(blank=True, null=True, verbose_name='Описание канала')
    # linked_chat_id = models.BigIntegerField(blank=True, null=True, verbose_name='ID чата канала')
    participants_count = models.IntegerField(default=0, verbose_name='Количество подписчиков')
    # photo_url = models.URLField(max_length=512, blank=True, null=True, verbose_name='Ссылка на фото')
    parsed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата парсинга')
    pinned_messages = models.JSONField(blank=True, null=True, default=list, verbose_name='Закрепленное сообщение')
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата создания')
    last_messages = models.JSONField(blank=True, null=True, default=list, verbose_name='Последние сообщения')
    average_views = models.IntegerField(default=0, verbose_name='Среднее количество просмотров')

    class Meta:
        verbose_name = 'Telegram канал'
        verbose_name_plural = 'Telegram каналы'

    def last_stat(self):
        """Получение последней статистики канала"""
        return self.channelstats_set.order_by('-parsed_at').first()

    def __str__(self):
        return f"{self.channel_id} канал {self.title}"


class ChannelStats(models.Model):
    channel = models.ForeignKey(TelegramChannel, on_delete=models.CASCADE, verbose_name="Канал")
    participants_count = models.IntegerField(verbose_name="Количество участников")
    daily_growth = models.IntegerField(default=0, verbose_name="Прирост за день")
    parsed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Статистика канала"
        verbose_name_plural = "Статистика каналов"
        get_latest_by = 'parsed_at'
        ordering = ['-parsed_at']

    def __str__(self):
        return f"{self.channel} - {self.parsed_at}"


# Create your models here.

