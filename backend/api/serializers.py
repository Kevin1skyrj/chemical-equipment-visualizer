"""Serializers for dataset endpoints."""

from rest_framework import serializers

from .models import Dataset


class DatasetSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            "id",
            "name",
            "source_filename",
            "uploaded_at",
            "total_records",
            "avg_flowrate",
            "avg_pressure",
            "avg_temperature",
            "type_distribution",
            "metrics",
        ]


class DatasetDetailSerializer(DatasetSummarySerializer):
    records = serializers.JSONField()

    class Meta(DatasetSummarySerializer.Meta):
        fields = DatasetSummarySerializer.Meta.fields + ["records"]


class DatasetUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    file = serializers.FileField()

    def validate_file(self, file):
        if not file.name.lower().endswith(".csv"):
            raise serializers.ValidationError("Only CSV uploads are supported.")
        return file
