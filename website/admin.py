from django.contrib import admin
from .models import SiteMeta, Page, PageSection, InfoCard
# Register your models here.
# admin.site.register(SiteMeta)
@admin.register(SiteMeta)
class SiteMetaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Page)

class InfoCardAdmin(admin.StackedInline):
    model = InfoCard

@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    inlines = [InfoCardAdmin]

    class Meta:
        model = PageSection

