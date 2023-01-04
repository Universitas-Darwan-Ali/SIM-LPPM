from django.contrib import admin
from .models import Bantuan
from django.utils.html import format_html

@admin.register(Bantuan)
class BantuanAdmin(admin.ModelAdmin):
    list_display = ['keterangan', 'Link_Berkas']
    search_fields = ['keterangan', 'link']
    list_filter = ['keterangan']

    def Link_Berkas(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.link,
            obj.link
        )
    Link_Berkas.allow_tags = True