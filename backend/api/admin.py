from django.contrib import admin

from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
	list_display = (
		"name",
		"source_filename",
		"uploaded_at",
		"total_records",
	)
	search_fields = ("name", "source_filename")
	ordering = ("-uploaded_at",)
