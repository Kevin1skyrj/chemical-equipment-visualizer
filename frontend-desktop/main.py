"""PyQt5 desktop client for the Chemical Equipment Parameter Visualizer."""

import base64
import os
import sys
from datetime import datetime

import pandas as pd
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")


def build_auth_headers():
    if not API_USERNAME or not API_PASSWORD:
        raise RuntimeError(
            "Set API_USERNAME and API_PASSWORD environment variables for Basic Auth."
        )
    token = base64.b64encode(f"{API_USERNAME}:{API_PASSWORD}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


class DistributionCanvas(FigureCanvas):
    def __init__(self):
        self.figure = Figure(figsize=(5, 3))
        super().__init__(self.figure)
        self.axes = self.figure.add_subplot(111)

    def update_chart(self, distribution: dict):
        self.axes.clear()
        if not distribution:
            self.axes.text(0.5, 0.5, "No data", ha="center", va="center")
        else:
            labels = list(distribution.keys())
            values = list(distribution.values())
            self.axes.bar(labels, values, color="#2563eb")
            self.axes.set_ylabel("Count")
            self.axes.set_title("Equipment Type Distribution")
            self.axes.tick_params(axis="x", rotation=30)
        self.figure.tight_layout()
        self.draw_idle()


class DatasetDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.resize(1200, 780)
        self.latest_dataset = None
        self.history = []
        self._build_ui()
        self.refresh_dashboard()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(16)

        self.upload_group = self._build_upload_group()
        layout.addWidget(self.upload_group)

        summary_section = QGroupBox("Latest Dataset Summary")
        summary_layout = QGridLayout(summary_section)
        self.summary_labels = {
            "records": QLabel("-"),
            "flowrate": QLabel("-"),
            "pressure": QLabel("-"),
            "temperature": QLabel("-"),
            "uploaded": QLabel("-"),
        }
        summary_layout.addWidget(QLabel("Uploaded"), 0, 0)
        summary_layout.addWidget(self.summary_labels["uploaded"], 0, 1)
        summary_layout.addWidget(QLabel("Total Records"), 0, 2)
        summary_layout.addWidget(self.summary_labels["records"], 0, 3)
        summary_layout.addWidget(QLabel("Avg Flowrate"), 1, 0)
        summary_layout.addWidget(self.summary_labels["flowrate"], 1, 1)
        summary_layout.addWidget(QLabel("Avg Pressure"), 1, 2)
        summary_layout.addWidget(self.summary_labels["pressure"], 1, 3)
        summary_layout.addWidget(QLabel("Avg Temperature"), 2, 0)
        summary_layout.addWidget(self.summary_labels["temperature"], 2, 1)
        layout.addWidget(summary_section)

        self.chart = DistributionCanvas()
        layout.addWidget(self.chart)

        self.records_table = QTableWidget()
        self.records_table.setAlternatingRowColors(True)
        self.records_table.setColumnCount(0)
        self.records_table.setRowCount(0)
        self.records_table.setMinimumHeight(200)
        layout.addWidget(self.records_table)

        history_section = QGroupBox("Upload History (Last 5)")
        history_layout = QVBoxLayout(history_section)
        history_buttons = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_dashboard)
        self.report_button = QPushButton("Download PDF for Selected")
        self.report_button.clicked.connect(self.download_selected_report)
        history_buttons.addWidget(self.refresh_button)
        history_buttons.addWidget(self.report_button)
        history_layout.addLayout(history_buttons)
        self.history_list = QListWidget()
        self.history_list.itemSelectionChanged.connect(self._handle_history_selection)
        history_layout.addWidget(self.history_list)
        layout.addWidget(history_section)

    def _build_upload_group(self):
        group = QGroupBox("Upload CSV to Backend")
        grid = QGridLayout(group)

        self.name_input = QLineEdit()
        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)
        browse_button = QPushButton("Browse…")
        browse_button.clicked.connect(self._pick_file)
        upload_button = QPushButton("Upload")
        upload_button.clicked.connect(self._upload_file)

        grid.addWidget(QLabel("Dataset Name"), 0, 0)
        grid.addWidget(self.name_input, 0, 1, 1, 3)
        grid.addWidget(QLabel("CSV Path"), 1, 0)
        grid.addWidget(self.file_input, 1, 1, 1, 2)
        grid.addWidget(browse_button, 1, 3)
        grid.addWidget(upload_button, 2, 3)
        return group

    def _pick_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", filter="CSV Files (*.csv)")
        if file_path:
            self.file_input.setText(file_path)

    def _upload_file(self):
        file_path = self.file_input.text().strip()
        if not file_path:
            QMessageBox.warning(self, "Missing File", "Please choose a CSV file.")
            return
        try:
            headers = build_auth_headers()
            with open(file_path, "rb") as file_handle:
                files = {"file": file_handle}
                data = {}
                if self.name_input.text().strip():
                    data["name"] = self.name_input.text().strip()
                response = requests.post(
                    f"{API_BASE_URL}/datasets/upload/",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=20,
                )
                response.raise_for_status()
            QMessageBox.information(self, "Success", "Upload completed!")
            self.refresh_dashboard()
        except Exception as exc:
            QMessageBox.critical(self, "Upload Failed", str(exc))

    def refresh_dashboard(self):
        try:
            headers = build_auth_headers()
        except RuntimeError as exc:
            QMessageBox.critical(self, "Auth Missing", str(exc))
            return

        try:
            latest = requests.get(
                f"{API_BASE_URL}/datasets/latest/", headers=headers, timeout=15
            )
            if latest.status_code == 404:
                self.latest_dataset = None
            else:
                latest.raise_for_status()
                self.latest_dataset = latest.json()
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to load latest dataset: {exc}")
            return

        try:
            history = requests.get(
                f"{API_BASE_URL}/datasets/history/", headers=headers, timeout=15
            )
            history.raise_for_status()
            self.history = history.json()
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to load history: {exc}")
            return

        self._render_latest_dataset()
        self._render_history()

    def _render_latest_dataset(self):
        if not self.latest_dataset:
            for label in self.summary_labels.values():
                label.setText("-")
            self.records_table.setRowCount(0)
            self.records_table.setColumnCount(0)
            self.chart.update_chart({})
            return

        ds = self.latest_dataset
        self.summary_labels["records"].setText(str(ds["total_records"]))
        self.summary_labels["flowrate"].setText(f"{ds['avg_flowrate']} m3/h")
        self.summary_labels["pressure"].setText(f"{ds['avg_pressure']} bar")
        self.summary_labels["temperature"].setText(f"{ds['avg_temperature']} °C")
        uploaded = datetime.fromisoformat(ds["uploaded_at"].replace("Z", "+00:00"))
        self.summary_labels["uploaded"].setText(uploaded.strftime("%d %b %Y %H:%M"))

        records = pd.DataFrame(ds["records"])
        self.records_table.setRowCount(min(len(records), 100))
        self.records_table.setColumnCount(len(records.columns))
        self.records_table.setHorizontalHeaderLabels(records.columns)
        for row_index in range(min(len(records), 100)):
            for col_index, column in enumerate(records.columns):
                value = str(records.iloc[row_index][column])
                self.records_table.setItem(
                    row_index, col_index, QTableWidgetItem(value)
                )
        self.records_table.resizeColumnsToContents()

        self.chart.update_chart(ds.get("type_distribution", {}))

    def _render_history(self):
        self.history_list.clear()
        for dataset in self.history:
            title = f"{dataset['name']} ({dataset['total_records']} records)"
            timestamp = datetime.fromisoformat(dataset["uploaded_at"].replace("Z", "+00:00"))
            item = QListWidgetItem(f"{title}\n{timestamp:%d %b %Y %H:%M}")
            item.setData(Qt.UserRole, dataset)
            self.history_list.addItem(item)

    def _handle_history_selection(self):
        selected = self.history_list.currentItem()
        if not selected:
            return
        dataset = selected.data(Qt.UserRole)
        if not dataset:
            return
        QMessageBox.information(
            self,
            dataset["name"],
            f"Records: {dataset['total_records']}\n"
            f"Avg Flowrate: {dataset['avg_flowrate']}\n"
            f"Avg Temperature: {dataset['avg_temperature']}",
        )

    def download_selected_report(self):
        selected = self.history_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Select Dataset", "Choose a dataset first.")
            return
        dataset = selected.data(Qt.UserRole)
        try:
            headers = build_auth_headers()
            response = requests.get(
                f"{API_BASE_URL}/datasets/{dataset['id']}/report/",
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF Report",
                f"{dataset['name']}.pdf",
                filter="PDF Files (*.pdf)",
            )
            if save_path:
                with open(save_path, "wb") as file_handle:
                    file_handle.write(response.content)
                QMessageBox.information(self, "Saved", "Report downloaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Download Failed", str(exc))


def main():
    app = QApplication(sys.argv)
    window = DatasetDashboard()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
