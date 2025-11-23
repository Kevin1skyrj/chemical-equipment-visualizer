from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Dataset
from .services import create_dataset_from_file

SAMPLE_CSV = b"""Equipment Name,Type,Flowrate,Pressure,Temperature\nPump-1,Pump,120,5.2,110\n"""



class DatasetServiceTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="service-user", email="service@example.com", password="pass1234"
		)

	def test_create_dataset_from_file_persists_metrics(self):
		file_obj = SimpleUploadedFile("test.csv", SAMPLE_CSV, content_type="text/csv")
		dataset = create_dataset_from_file(
			file_obj=file_obj, owner=self.user, name="Test Dataset"
		)

		self.assertEqual(dataset.total_records, 1)
		self.assertAlmostEqual(dataset.avg_flowrate, 120.0)
		self.assertIn("Pump", dataset.type_distribution)

	def test_history_limit_keeps_latest_five_per_owner(self):
		for idx in range(6):
			csv = SAMPLE_CSV.replace(b"Pump-1", f"Pump-{idx}".encode())
			file_obj = SimpleUploadedFile(f"test-{idx}.csv", csv, content_type="text/csv")
			create_dataset_from_file(
				file_obj=file_obj,
				owner=self.user,
				name=f"Dataset {idx}",
			)

		self.assertEqual(Dataset.objects.count(), 5)
		newest_name = Dataset.objects.order_by("-uploaded_at").first().name
		self.assertEqual(newest_name, "Dataset 5")

	def test_other_user_datasets_are_preserved(self):
		other = get_user_model().objects.create_user(
			username="second", email="second@example.com", password="pass1234"
		)
		file_obj = SimpleUploadedFile("test.csv", SAMPLE_CSV, content_type="text/csv")
		create_dataset_from_file(file_obj=file_obj, owner=other, name="Other Dataset")

		for idx in range(5):
			csv = SAMPLE_CSV.replace(b"Pump-1", f"Pump-{idx}".encode())
			file_obj = SimpleUploadedFile(f"self-{idx}.csv", csv, content_type="text/csv")
			create_dataset_from_file(
				file_obj=file_obj,
				owner=self.user,
				name=f"Dataset {idx}",
			)

		self.assertEqual(Dataset.objects.filter(owner=other).count(), 1)


class DatasetAPITests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			username="tester", email="tester@example.com", password="strong-pass"
		)
		self.client.force_authenticate(user=self.user)

	def test_upload_endpoint_returns_dataset_payload(self):
		url = reverse("dataset-upload")
		response = self.client.post(
			url,
			{"name": "API dataset", "file": SimpleUploadedFile("api.csv", SAMPLE_CSV)},
			format="multipart",
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data["name"], "API dataset")

	def test_latest_endpoint_returns_404_when_no_data(self):
		url = reverse("dataset-latest")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
