from django.contrib import admin

from .models import App


class AppAdmin(admin.ModelAdmin):

    list_display = ('name', 'total_models', 'created_at', 'updated_at')
    list_filter = ('created_at', )

admin.site.register(App, AppAdmin)
