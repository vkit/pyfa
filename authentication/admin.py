from django.contrib import admin

from .models import BaseTemplate, Tab, SubTab


class TabInline(admin.TabularInline):
    model = Tab


class SubTabInline(admin.TabularInline):
    model = SubTab


class BaseTemplateAdmin(admin.ModelAdmin):
    inlines = [
        TabInline,
    ]


class TabAdmin(admin.ModelAdmin):
    inlines = [
        SubTabInline,
    ]

admin.site.register(BaseTemplate, BaseTemplateAdmin)
admin.site.register(Tab, TabAdmin)

