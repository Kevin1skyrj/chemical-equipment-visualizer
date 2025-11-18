"""Domain helpers for parsing CSV files and persisting datasets."""

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO, Dict, Tuple

import pandas as pd
from django.core.files.base import ContentFile
from django.db import transaction

from .models import Dataset

REQUIRED_COLUMNS = {
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature",
}

COLUMN_RENAMES = {
    "Equipment Name": "equipment_name",
    "Type": "equipment_type",
    "Flowrate": "flowrate",
    "Pressure": "pressure",
    "Temperature": "temperature",
}

def _load_dataframe(file_bytes: bytes) -> pd.DataFrame:
    buffer = io.BytesIO(file_bytes)
    df = pd.read_csv(buffer)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

    df = df[list(COLUMN_RENAMES.keys())].rename(columns=COLUMN_RENAMES)
    for column in ("flowrate", "pressure", "temperature"):
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df.empty:
        raise ValueError("CSV must include at least one equipment row.")

    if df[["flowrate", "pressure", "temperature"]].isnull().any().any():
        raise ValueError("Numeric columns contain invalid values. Please clean the CSV.")

    df["flowrate"] = df["flowrate"].round(2)
    df["pressure"] = df["pressure"].round(2)
    df["temperature"] = df["temperature"].round(2)
    return df


def _compute_metrics(df: pd.DataFrame) -> Tuple[Dict, Dict]:
    totals = {
        "total_records": int(df.shape[0]),
        "avg_flowrate": round(df["flowrate"].mean(), 2),
        "avg_pressure": round(df["pressure"].mean(), 2),
        "avg_temperature": round(df["temperature"].mean(), 2),
    }
    type_distribution = df["equipment_type"].value_counts().sort_index().to_dict()

    def _extreme(column: str, agg_func: str) -> Dict:
        idx_func = df[column].idxmax if agg_func == "max" else df[column].idxmin
        idx = idx_func()
        row = df.loc[idx]
        return {
            "equipment_name": row["equipment_name"],
            "equipment_type": row["equipment_type"],
            column: row[column],
        }

    metrics = {
        "max_flowrate": _extreme("flowrate", "max"),
        "min_flowrate": _extreme("flowrate", "min"),
        "max_temperature": _extreme("temperature", "max"),
    }
    return totals | {"type_distribution": type_distribution}, metrics


@transaction.atomic
def create_dataset_from_file(*, file_obj: BinaryIO, name: str | None = None) -> Dataset:
    """Parse the CSV, persist the dataset, and return the instance."""

    raw_bytes = file_obj.read()
    if not raw_bytes:
        raise ValueError("Uploaded file is empty.")

    df = _load_dataframe(raw_bytes)
    totals, metrics = _compute_metrics(df)
    records = df.to_dict(orient="records")

    safe_filename = Path(getattr(file_obj, "name", "uploaded.csv")).name
    display_name = name or Path(safe_filename).stem.replace("_", " ").title()

    stored_file = ContentFile(raw_bytes)
    stored_file.name = safe_filename

    dataset = Dataset.objects.create(
        name=display_name,
        source_filename=safe_filename,
        original_file=stored_file,
        total_records=totals["total_records"],
        avg_flowrate=totals["avg_flowrate"],
        avg_pressure=totals["avg_pressure"],
        avg_temperature=totals["avg_temperature"],
        type_distribution=totals["type_distribution"],
        metrics=metrics,
        records=records,
    )
    return dataset
