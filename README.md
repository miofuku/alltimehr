# AI HR Agent

An AI-powered HR system for resume screening and interview management.

## Features

- Automatic resume parsing and analysis
- Smart scoring system
- Education background analysis
- Work experience evaluation
- Skills matching
- Cover letter evaluation (optional)
- Automated interview scheduling
- Email notifications
- Calendar integration

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Google Calendar API credentials
- SMTP server access

## Setup

### Backend Setup

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Spacy model:
```bash
python -m spacy download en_core_web_lg
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

5. Set up Google Calendar credentials:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Calendar API
   - Create credentials (OAuth 2.0)
   - Download credentials and save as `credentials.json`
   - Update `GOOGLE_CALENDAR_CREDS_FILE` in `.env`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configurations
```

## Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Start Frontend Development Server

```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Backend Development

- API endpoints are in `backend/app/api/`
- Data models are in `backend/app/models/`
- Business logic is in `backend/app/services/`
- Utility functions are in `backend/app/utils/`

### Frontend Development

- Components are in `frontend/src/components/`
- Pages are in `frontend/src/pages/`
- Utility functions are in `frontend/src/utils/`


## License

MIT License