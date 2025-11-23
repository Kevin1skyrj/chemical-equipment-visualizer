from io import BytesIO

from django.http import FileResponse, Http404
from rest_framework import generics, parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset
from .pdf import build_dataset_report
from .serializers import (
	DatasetDetailSerializer,
	DatasetSummarySerializer,
	DatasetUploadSerializer,
)
from .services import create_dataset_from_file


class DatasetUploadView(APIView):
	parser_classes = [parsers.MultiPartParser, parsers.FormParser]

	def post(self, request, *args, **kwargs):
		serializer = DatasetUploadSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		try:
			dataset = create_dataset_from_file(
				file_obj=serializer.validated_data["file"],
				owner=request.user,
				name=serializer.validated_data.get("name"),
			)
		except ValueError as exc:
			return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

		return Response(
			DatasetDetailSerializer(dataset).data,
			status=status.HTTP_201_CREATED,
		)


class LatestDatasetView(generics.RetrieveAPIView):
	serializer_class = DatasetDetailSerializer

	def get_queryset(self):
		return Dataset.objects.filter(owner=self.request.user)

	def get_object(self):
		dataset = self.get_queryset().order_by("-uploaded_at").first()
		if not dataset:
			raise Http404("No datasets have been uploaded yet.")
		return dataset


class DatasetHistoryView(generics.ListAPIView):
	serializer_class = DatasetSummarySerializer

	def get_queryset(self):
		return Dataset.objects.filter(owner=self.request.user)


class DatasetDetailView(generics.RetrieveAPIView):
	serializer_class = DatasetDetailSerializer
	lookup_field = "pk"

	def get_queryset(self):
		return Dataset.objects.filter(owner=self.request.user)


class DatasetReportView(APIView):
	def get(self, request, pk):
		try:
			dataset = Dataset.objects.get(pk=pk, owner=request.user)
		except Dataset.DoesNotExist as exc:
			raise Http404("Dataset not found") from exc

		pdf_bytes = build_dataset_report(dataset)
		buffer = BytesIO(pdf_bytes)
		filename = f"dataset-report-{dataset.uploaded_at:%Y%m%d%H%M%S}.pdf"
		return FileResponse(buffer, as_attachment=True, filename=filename)
