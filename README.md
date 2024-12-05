# AI HR Agent

An AI-powered HR system for resume screening and interview management.

## Features

- Intelligent resume parsing and analysis using LangGraph
- Smart scoring system with skills matching
- Education and experience evaluation
- Automated interview scheduling
- Email notifications
- Calendar integration with Google Calendar
- Video interview setup

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- OpenAI API key
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

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations:
# - Add your OpenAI API key
# - Configure SMTP settings
# - Set up secret key (use: python -c "import secrets; print(secrets.token_hex(32))")
```

4. Set up Google Calendar credentials:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Calendar API
   - Create credentials (OAuth 2.0)
   - Download credentials and save as `credentials.json` in `backend/credentials/`
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
# Configure your environment variables
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
- Utility functions are in `frontend/src/utils/`

## License

MIT License
