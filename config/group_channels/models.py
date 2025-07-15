from django.db import models
from config.users.models import User
# from config.channel.models import Channel
# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='именем')
    description = models.CharField(max_length=200, verbose_name='описанием')
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_group',
        verbose_name='Владелец',
        null=True,
        blank=True,
    )
    # channels = models.ManyToManyField(
    #     Channel,
    #     verbose_name='Каналы',
    #     related_name='group_channels',
    #     blank=True,
    # )
    image_url = models.CharField(verbose_name='обложка группы')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'groups'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    
    def __str__(self):
        return self.name