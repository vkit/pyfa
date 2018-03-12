from django.contrib import admin

from modeller.models import ModelObject, ModelField


class ModelFieldInline(admin.TabularInline):
    model = ModelField
    extra = 3


class ModelObjectAdmin(admin.ModelAdmin):

    inlines = [ModelFieldInline]
    list_display = ('name', 'app', 'created_at', 'updated_at')
    list_filter = ('app', 'created_at')

admin.site.register(ModelObject, ModelObjectAdmin)
