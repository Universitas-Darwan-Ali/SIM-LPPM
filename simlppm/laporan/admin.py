from django.contrib import admin
from .models import Detil
from django.utils.html import format_html

@admin.register(Detil)
class DetilAdmin(admin.ModelAdmin):
    list_display = ['Laporan', 'Link_Berkas']
    search_fields = ['Laporan', 'Link']
    list_filter = ['Laporan']

    def Link_Berkas(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.Link,
            obj.Link
        )
    Link_Berkas.allow_tags = True