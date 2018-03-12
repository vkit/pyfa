from django.contrib import admin

from .models import Page


class PageAdmin(admin.ModelAdmin):

    list_display = ('name', 'app', 'model', 'created_at', 'updated_at')
    list_filter = ('created_at', )

admin.site.register(Page, PageAdmin)
