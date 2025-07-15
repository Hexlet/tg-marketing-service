from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    avatar_image = models.CharField(verbose_name='url изображения профиля', blank=True, null=True)
    role = models.CharField(verbose_name='роль',
                            max_length=150)
    bio = models.CharField(max_length=200, verbose_name='о себе', blank=True)
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.get_full_name()