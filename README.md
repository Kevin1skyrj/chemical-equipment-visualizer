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
python manage.py seed_sample_data --username admin  # loads sample_equipment_data.csv for an owner
python manage.py runserver
```

> Every API call requires HTTP Basic authentication. Use the credentials you created via `createsuperuser`. Frontend apps should store them in environment variables and send the `Authorization` header with each request.

### Local Quickstart (what I run before each test)
1. `cd backend && .\.venv\Scripts\Activate.ps1`
2. `python manage.py createsuperuser` — create the reviewer account (`admin/AdminPassword123!` or any pair you like).
3. `python manage.py seed_sample_data --username <your-user>` — preloads `sample_equipment_data.csv` so the dashboard has something to render immediately.
4. `python manage.py runserver` — leave this tab running.
5. In a new terminal: `cd frontend-web && npm install && npm run dev`.
6. Visit `http://localhost:5173`, sign in with the credentials from step 2, upload a CSV, view the charts/history, and download the PDF.
7. Use the **Signed in as … · Sign out** chip in the top-right of the dashboard whenever you want to switch accounts or clear saved credentials.

### Demo Credentials / Sharing Access

- Run `python manage.py createsuperuser --username demo_admin` (replace `demo_admin` with any label you like) and set a password that you can share privately.
- Use the same username/password pair inside both the web dashboard (login screen) and the desktop client (either via environment variables or the credential prompt).
- When submitting the screening task, include these demo credentials in your submission so evaluators can log in immediately without recreating users. The login screen now shows the credential pair (if you bundle them via `VITE_API_USERNAME` / `VITE_API_PASSWORD`) so reviewers see exactly what to use.
- Rotate or delete the demo account after the review period if you continue working on the project.

### Login & Per-user History

- The dashboard is gated behind a dedicated login page. Enter your Django credentials (or rely on `VITE_API_USERNAME`/`VITE_API_PASSWORD` during deployments) and click **Sign In**. Values live only in the current browser profile.
- Each dataset belongs to the authenticated Django user. The API, web dashboard, and desktop client always filter responses to "your" uploads and keep the five most recent datasets **per user**.
- The login page shows two tips: hosted builds list the reviewer credentials that were bundled at build time, and local builds remind you to run `python manage.py createsuperuser`. The dashboard now highlights your current identity in the header ("Signed in as …") with a one-click **Sign out** action so you can switch users quickly.

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
> Tip: If you don't want credentials baked into `.env`, launch the dev server and sign in through the web login screen. The credentials stay in `localStorage` for that browser profile only.

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

## Feature Checklist (matches screening brief)
1. **CSV Upload (Web + Desktop)** &mdash; both clients send multipart CSVs to `/api/datasets/upload/`.
2. **Data Summary API** &mdash; backend computes totals, averages, and distribution for every dataset.
3. **Visualization** &mdash; React uses Chart.js + tables, PyQt5 uses Matplotlib + Qt tables.
4. **History Management** &mdash; model enforces “last five uploads only” after every save.
5. **PDF + Basic Auth** &mdash; `/api/datasets/<id>/report/` streams a ReportLab PDF and DRF enforces HTTP Basic authentication globally.
6. **Sample CSV workflow** &mdash; `python manage.py seed_sample_data` ingests `sample_equipment_data.csv` for immediate demos.

> ✅ All mandatory features from the PDF are implemented and covered by either automated tests or documented manual steps.

## Demo & Recording Guide
Use these steps when capturing screenshots or the final walk-through video:

1. **Start backend**: `cd backend && .\.venv\Scripts\Activate.ps1 && python manage.py runserver`.
2. **Seed sample data** (optional if already done): `python manage.py seed_sample_data --username admin` (replace `admin` with any existing user).
3. **Web app**:
	- `cd frontend-web && npm install && npm run dev`.
	- Visit the login screen, enter your Django username/password, and click *Sign In*.
	- Upload `sample_equipment_data.csv`, show the summary cards, Chart.js bar chart, records table, PDF download, and history refresh.
4. **Desktop app**:
	- `cd frontend-desktop && .\.venv\Scripts\Activate.ps1 && pip install -r requirements.txt && python main.py`.
	- When the credentials dialog appears, enter the same username/password.
	- Demonstrate loading the seeded dataset, uploading a new CSV, viewing metrics, and saving a PDF report.
5. Conclude the recording by showing the backend logs (confirming authenticated requests) and mentioning Basic Auth usage.

## Deployment Prep (for later)
1. **Backend**
	- Set `DEBUG=False`, `ALLOWED_HOSTS`, and production `SECRET_KEY` in environment variables.
	- Configure static collection (`python manage.py collectstatic`) and persistent media storage (S3/Azure Blob/local volume).
	- Provide Basic Auth credentials via environment variables or the target platform’s secret store.
2. **Web Frontend**
	- Set `VITE_API_BASE_URL` to the deployed API URL, rebuild with `npm run build`, and deploy the `dist/` folder (Vercel, Netlify, Azure Static Web Apps, etc.).
3. **Desktop Client**
	- Update `.env`/system variables (or rely on the runtime prompt) with the public API URL and production credentials.
4. **Verification**
	- Run `python manage.py test`, `npm run build`, and a full manual smoke test before sharing the live link.
5. **Submission**
	- Include the GitHub repo URL, hosted web URL, API Base URL, desktop demo video, and credentials (shared privately) in the screening form.

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
- Developer: Rajat Pandey
- Email: rajatpndey257@gmail.com
- GitHub: https://github.com/Kevin1skyrj

## Acknowledgments
- FOSSEE (Free and Open Source Software for Education)
- IIT Bombay
