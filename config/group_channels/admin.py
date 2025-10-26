from django.contrib import admin

# Register your models here.
from .models import Group, AutoGroupRule

# Register your models here.

class AutoGroupRule(admin.StackedInline):
    model = AutoGroupRule
    can_delete = False
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_editorial', 'order', 'owner')
    list_filter = ('is_editorial',)
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    filter_horizontal = ('channels',)

    def get_readonly_fields(self, request, obj = None):
        ro = super().get_readonly_fields(request, obj) or []
        if obj and hasattr(obj, 'auto_rule'):
            return tuple(set(ro) | {'channels'})
        return ro