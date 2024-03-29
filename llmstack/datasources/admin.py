from django.contrib import admin

from .models import DataSource, DataSourceEntry, DataSourceEntryFiles, DataSourceType


@admin.register(DataSourceEntry)
class DataSourceEntryAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "name", "datasource__name"]
    list_display = ["name"]


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "owner__email"]


@admin.register(DataSourceType)
class DataSourceTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(DataSourceEntryFiles)
class DataSourceEntryFilesAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "ref_id", "file"]
    list_display = ["uuid", "ref_id", "file", "created_at"]
