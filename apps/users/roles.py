from django.db import models

from models import User

"""Модели ролей и модель истории ролей"""
class Role(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
    

class UserRoleHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата назначения')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата снятия')
    reason = models.CharField(max_length=100, null=True)
    
    class Meta:
        verbose_name = 'История роли'
        verbose_name_plural = 'История ролей'