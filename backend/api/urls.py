from django.urls import path

from . import views

urlpatterns = [
    path("datasets/upload/", views.DatasetUploadView.as_view(), name="dataset-upload"),
    path("datasets/latest/", views.LatestDatasetView.as_view(), name="dataset-latest"),
    path("datasets/history/", views.DatasetHistoryView.as_view(), name="dataset-history"),
    path("datasets/<uuid:pk>/", views.DatasetDetailView.as_view(), name="dataset-detail"),
    path("datasets/<uuid:pk>/report/", views.DatasetReportView.as_view(), name="dataset-report"),
]
