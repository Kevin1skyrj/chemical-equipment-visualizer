from uuid import uuid4

from django.db import models
from django.utils import timezone


def dataset_upload_path(instance, filename):
	timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
	return f"datasets/{timestamp}_{filename}"


class Dataset(models.Model):
	"""Persist parsed CSV data, summary metrics, and original file reference."""

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	name = models.CharField(max_length=255)
	source_filename = models.CharField(max_length=255)
	original_file = models.FileField(upload_to=dataset_upload_path)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	total_records = models.PositiveIntegerField()
	avg_flowrate = models.FloatField()
	avg_pressure = models.FloatField()
	avg_temperature = models.FloatField()
	type_distribution = models.JSONField(default=dict)
	metrics = models.JSONField(default=dict, blank=True)
	records = models.JSONField()

	class Meta:
		ordering = ["-uploaded_at"]

	def __str__(self):
		return f"{self.name} ({self.total_records} records)"

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		preserved_ids = (
			Dataset.objects.order_by("-uploaded_at").values_list("id", flat=True)[:5]
		)
		Dataset.objects.exclude(id__in=preserved_ids).delete()
