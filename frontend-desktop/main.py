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
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QDialog,
    QDialogButtonBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from styles import DASHBOARD_QSS

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")


class CredentialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter API Credentials")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Enter the Django admin username/password for the API."))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_credentials(self):
        return self.username_input.text().strip(), self.password_input.text().strip()


def build_auth_headers(parent=None):
    global API_USERNAME, API_PASSWORD
    if not API_USERNAME or not API_PASSWORD:
        dialog = CredentialDialog(parent)
        if dialog.exec_() == QDialog.Accepted:
            username, password = dialog.get_credentials()
            if not username or not password:
                raise RuntimeError("Username and password are required for Basic Auth.")
            API_USERNAME, API_PASSWORD = username, password
        else:
            raise RuntimeError(
                "Set API_USERNAME and API_PASSWORD env vars or provide them when prompted."
            )
    token = base64.b64encode(f"{API_USERNAME}:{API_PASSWORD}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


class DistributionCanvas(FigureCanvas):
    def __init__(self):
        self.figure = Figure(figsize=(5, 3), facecolor="none")
        super().__init__(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_facecolor("#ffffff")
        for spine in self.axes.spines.values():
            spine.set_color("#e2e8f0")
            spine.set_linewidth(1.2)

    def update_chart(self, distribution: dict):
        self.axes.clear()
        self.axes.set_facecolor("#ffffff")
        if not distribution:
            self.axes.text(0.5, 0.5, "No data", ha="center", va="center", color="#64748b", fontsize=12)
        else:
            labels = list(distribution.keys())
            values = list(distribution.values())
            bars = self.axes.bar(labels, values, color="#3b82f6", edgecolor="none", width=0.6)
            for bar in bars:
                bar.set_alpha(0.9)
            self.axes.set_ylabel("Count", fontsize=11, color="#64748b", fontweight="600")
            self.axes.tick_params(axis="x", rotation=30, labelsize=10, colors="#475569")
            self.axes.tick_params(axis="y", labelsize=10, colors="#475569")
            self.axes.grid(axis="y", alpha=0.2, linestyle="--", linewidth=0.8, color="#cbd5e1")
            for spine in self.axes.spines.values():
                spine.set_color("#e2e8f0")
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
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        layout.addWidget(self._build_hero_header())
        layout.addWidget(self._build_upload_card())
        layout.addWidget(self._build_summary_card())
        layout.addWidget(self._build_chart_card())
        layout.addWidget(self._build_records_card())
        layout.addWidget(self._build_history_card())
        layout.addStretch()

    def _styled_card(self, object_name="Card"):
        frame = QFrame()
        frame.setObjectName(object_name)
        return frame

    def _build_hero_header(self):
        frame = self._styled_card("HeroCard")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        eyebrow = QLabel("DESKTOP DASHBOARD")
        eyebrow.setObjectName("HeroEyebrow")
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setObjectName("HeroTitle")
        subtitle = QLabel(
            "Upload CSVs, explore real-time summaries, and download PDF insights directly from your desktop."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("HeroSubtitle")
        meta = QLabel(f"Connected to: {API_BASE_URL}")
        meta.setObjectName("HeroMeta")

        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addSpacing(4)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(meta)
        return frame

    def _build_upload_card(self):
        frame = self._styled_card()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Upload CSV to Backend")
        title.setObjectName("SectionTitle")
        subtitle = QLabel("Give the dataset a friendly name, pick a CSV, and send it to the API in one click.")
        subtitle.setObjectName("SectionSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Sample Equipment Data")
        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)
        self.file_input.setPlaceholderText("Select a CSV file...")
        browse_button = QPushButton("Browse…")
        browse_button.setProperty("variant", "ghost")
        browse_button.clicked.connect(self._pick_file)
        upload_button = QPushButton("Upload")
        upload_button.clicked.connect(self._upload_file)

        form.addWidget(QLabel("Dataset Name"), 0, 0)
        form.addWidget(self.name_input, 0, 1, 1, 3)
        form.addWidget(QLabel("CSV File"), 1, 0)
        form.addWidget(self.file_input, 1, 1, 1, 2)
        form.addWidget(browse_button, 1, 3)
        
        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(upload_button)
        
        layout.addLayout(form)
        layout.addLayout(button_row)
        return frame

    def _build_summary_card(self):
        frame = self._styled_card()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        header = QLabel("Latest Dataset Summary")
        header.setObjectName("SectionTitle")
        layout.addWidget(header)

        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(12)

        self.summary_labels = {
            "records": QLabel("-"),
            "flowrate": QLabel("-"),
            "pressure": QLabel("-"),
            "temperature": QLabel("-"),
            "uploaded": QLabel("-"),
        }

        for label in self.summary_labels.values():
            label.setStyleSheet("font-weight: 600; color: #0f172a;")

        grid.addWidget(QLabel("Uploaded"), 0, 0)
        grid.addWidget(self.summary_labels["uploaded"], 0, 1)
        grid.addWidget(QLabel("Total Records"), 0, 2)
        grid.addWidget(self.summary_labels["records"], 0, 3)
        grid.addWidget(QLabel("Avg Flowrate"), 1, 0)
        grid.addWidget(self.summary_labels["flowrate"], 1, 1)
        grid.addWidget(QLabel("Avg Pressure"), 1, 2)
        grid.addWidget(self.summary_labels["pressure"], 1, 3)
        grid.addWidget(QLabel("Avg Temperature"), 2, 0)
        grid.addWidget(self.summary_labels["temperature"], 2, 1)
        
        layout.addLayout(grid)
        return frame

    def _build_chart_card(self):
        frame = self._styled_card()
        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(12)
        header = QLabel("Equipment Type Distribution")
        header.setObjectName("SectionTitle")
        vbox.addWidget(header)
        self.chart = DistributionCanvas()
        self.chart.setMinimumHeight(280)
        vbox.addWidget(self.chart)
        return frame

    def _build_records_card(self):
        frame = self._styled_card()
        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(12)
        header = QLabel("Detailed Records (first 100)")
        header.setObjectName("SectionTitle")
        vbox.addWidget(header)
        self.records_table = QTableWidget()
        self.records_table.setAlternatingRowColors(True)
        self.records_table.setColumnCount(0)
        self.records_table.setRowCount(0)
        self.records_table.setMinimumHeight(240)
        self.records_table.verticalHeader().setDefaultSectionSize(32)
        vbox.addWidget(self.records_table)
        return frame

    def _build_history_card(self):
        frame = self._styled_card()
        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(12)
        header_row = QHBoxLayout()
        title = QLabel("Upload History (Last 5)")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setProperty("variant", "ghost")
        self.refresh_button.clicked.connect(self.refresh_dashboard)
        self.report_button = QPushButton("Download PDF")
        self.report_button.clicked.connect(self.download_selected_report)
        header_row.addWidget(self.refresh_button)
        header_row.addSpacing(8)
        header_row.addWidget(self.report_button)
        vbox.addLayout(header_row)

        self.history_list = QListWidget()
        self.history_list.itemSelectionChanged.connect(self._handle_history_selection)
        self.history_list.setMinimumHeight(180)
        vbox.addWidget(self.history_list)
        return frame

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
            headers = build_auth_headers(self)
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
            headers = build_auth_headers(self)
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
            headers = build_auth_headers(self)
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
    app.setStyleSheet(DASHBOARD_QSS)
    window = DatasetDashboard()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
