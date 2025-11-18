# Chemical Equipment Parameter Visualizer

A web and desktop application for visualizing chemical equipment parameters, developed as part of the FOSSEE Winter Internship screening task.

## Project Structure

```
chemical-equipment-visualizer/
├── backend/              # Django backend API
├── frontend-web/         # React + Vite web application
├── frontend-desktop/     # Desktop application
├── README.md
└── .gitignore
```

## Tech Stack

### Backend
- **Framework**: Django
- **API**: Django REST Framework

### Frontend (Web)
- **Framework**: React
- **Build Tool**: Vite
- **Language**: JavaScript/TypeScript

### Frontend (Desktop)
- **Framework**: PyQt5
- **Visualization**: Matplotlib
- **Networking**: requests + pandas helpers

## Getting Started

### Prerequisites
- Python 3.x
- Node.js and npm
- Git

### Backend Setup
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # basic-auth user for all APIs
python manage.py seed_sample_data  # loads sample_equipment_data.csv
python manage.py runserver
```

> Every API call requires HTTP Basic authentication. Use the credentials you created via `createsuperuser`. Frontend apps should store them in environment variables and send the `Authorization` header with each request.

### Environment Variables

| Component | Keys |
| --- | --- |
| Web (Vite) | `VITE_API_BASE_URL`, `VITE_API_USERNAME`, `VITE_API_PASSWORD` (optional if you prefer entering credentials in the UI) |
| Desktop (PyQt5) | `API_BASE_URL`, `API_USERNAME`, `API_PASSWORD` |

If environment variables are omitted, both clients default to `http://127.0.0.1:8000/api` and will skip authentication (the backend will then reject the request). Always keep credentials out of source control by using `.env` files or shell exports.

### Frontend Web Setup
```bash
cd frontend-web
cp .env.example .env  # optional: pre-fill Basic Auth credentials
npm install
npm run dev
```
> Tip: If you don't want credentials baked into `.env`, launch the dev server and use the in-app **Backend Authentication** card to enter them. They are stored only in `localStorage` on that browser profile.

### Frontend Desktop Setup
```bash
cd frontend-desktop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
setx API_BASE_URL http://127.0.0.1:8000/api
setx API_USERNAME your-username
setx API_PASSWORD your-password
python main.py
```
> On macOS/Linux replace the environment variable commands with `export`.

## Features
- Upload CSV files from either frontend (React or PyQt5) to a shared Django backend.
- Backend analytics via Pandas (averages, distribution, extreme values) stored for the latest 5 datasets.
- Chart-ready REST API responses for Chart.js (web) and Matplotlib (desktop).
- PDF report generation endpoint plus basic authentication for secure submissions.

## Development

### Running the Backend
```bash
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

### Running the Frontend (Web)
```bash
cd frontend-web
npm run dev
```

## Backend API Surface

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/datasets/upload/` | `POST` | Multipart CSV upload (`file`, optional `name`). Parses the CSV, persists stats, returns the dataset payload. |
| `/api/datasets/latest/` | `GET` | Returns the most recent dataset including full records for immediate visualization. |
| `/api/datasets/history/` | `GET` | Lists summaries for the last five uploads (enforced automatically). |
| `/api/datasets/<id>/` | `GET` | Retrieve a specific dataset with all rows. |
| `/api/datasets/<id>/report/` | `GET` | Downloads a PDF report (generated on the fly with ReportLab). |

All endpoints require HTTP Basic authentication. Configure your frontend clients to include the header:

```
Authorization: Basic base64(username:password)
```

### Sample Data Workflow
1. The repository root ships with `sample_equipment_data.csv` from the screening document.
2. Run `python manage.py seed_sample_data` once to preload it into the backend.
3. Frontends can fetch `/api/datasets/latest/` immediately to render demo charts/tables.

## Contributing
This project is part of the FOSSEE Winter Internship screening task.


## Contact
- Developer: [Your Name]
- Email: [Your Email]
- GitHub: [Your GitHub Profile]

## Acknowledgments
- FOSSEE (Free and Open Source Software for Education)
- IIT Bombay
