from django.contrib import admin
from .models import Support
# Register your models here.
# admin.site.register(Support)
@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'subject')
    list_display_links = ('id', 'name', 'phone', 'email', 'subject')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False