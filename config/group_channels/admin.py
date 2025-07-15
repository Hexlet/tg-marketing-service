from django.contrib import admin

# Register your models here.
from .models import Group

# Register your models here.


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name',]