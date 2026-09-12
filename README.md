<<<<<<< HEAD
# Bluestock IPO Platform — FastAPI + React + MySQL + SQLAlchemy

End-to-end internship project for an IPO information platform. The implementation follows the uploaded Bluestock brief's functional scope while using the requested modern stack: **FastAPI, React, MySQL and SQLAlchemy**.

## Features
- Public IPO listing, search and status filtering
- IPO detail page with price band, dates, issue size, status and returns
- Listing gain and current return calculations
- RHP / DRHP PDF upload and viewing
- Admin JWT login
- Admin CRUD for IPO records
- Pagination-ready API parameters and ordering
- Health check
- MySQL database with SQLAlchemy ORM
- Docker Compose for MySQL + FastAPI + React
- OpenAPI/Swagger at `/docs`
- API tests
- Secure environment configuration
- Sample IPO seed data

## Project structure
```
bluestock-ipo-fastapi-react/
├── backend/
│   ├── app/
│   │   ├── api/          # Auth + IPO endpoints
│   │   ├── core/         # Configuration + JWT security
│   │   ├── db/           # SQLAlchemy engine/session
│   │   ├── models/       # ORM models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Seed helpers
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
├── sample_ipos.csv
└── docker-compose.yml
```

## Run with Docker
1. Install Docker Desktop.
2. From this directory run:
```bash
docker compose up --build
```
3. Open:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

Default admin:
- Email: `admin@bluestock.local`
- Password: `Admin@12345`

**Change the admin password and SECRET_KEY before any real deployment.**

## Run locally without Docker
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
uvicorn app.main:app --reload
```
Create a MySQL database matching `.env` first.

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/ipos` | List/search/filter IPOs |
| GET | `/api/v1/ipos/{id}` | IPO detail |
| GET | `/api/v1/ipos/stats` | Dashboard counts |
| POST | `/api/v1/ipos` | Admin create |
| PUT | `/api/v1/ipos/{id}` | Admin update |
| DELETE | `/api/v1/ipos/{id}` | Admin delete |
| POST | `/api/v1/ipos/{id}/documents/rhp` | Admin RHP upload |
| POST | `/api/v1/ipos/{id}/documents/drhp` | Admin DRHP upload |
| POST | `/api/v1/auth/login` | Admin JWT login |
| GET | `/health` | Service/database health |

## Query examples
`GET /api/v1/ipos?search=technology&status=listed&limit=20`

`GET /api/v1/ipos?sort=-listing_date`

## Testing
From `backend/`:
```bash
pytest
```

## Production checklist
- Use a strong random SECRET_KEY
- Replace demo admin credentials
- Put MySQL behind a private network
- Serve through HTTPS and a reverse proxy
- Store uploads in object storage such as S3-compatible storage
- Add structured logging and monitoring
- Configure trusted CORS origins only
- Add database migrations (Alembic) before schema changes in production
- Back up the database regularly

## Internship scope mapping
The uploaded brief calls for IPO information including company identity, price band, dates, issue size/type, listing data, status, returns and RHP/DRHP documents, plus a client frontend and admin functionality. This project implements those requirements with the requested FastAPI/React/MySQL/SQLAlchemy stack.
=======
# Movie Search App

The Movie Search App is a web application that allows users to discover and explore movies, TV shows, and web series. It provides features like searching for movies, browsing by genre, exploring top picks, and viewing detailed information about movies. The app uses the OMDB API to fetch movie data.

## Features

- **Home Page**: Displays a hero section with a dynamic background slideshow, a featured movie of the week, and top-rated movies.
- **Search Functionality**: Users can search for movies by title, genre, or language.
- **Genre Exploration**: Browse movies by genre (e.g., Action, Comedy, Drama, Horror, Romance, Thriller).
- **Language Exploration**: Explore movies by language (e.g., English, Spanish, French, Hindi, etc.).
- **Web Series Section**: Discover popular web series like Breaking Bad, Stranger Things, and The Witcher.
- **Movie Details**: View detailed information about a movie, including its plot, director, cast, IMDb rating, and more.
- **Responsive Design**: The app is fully responsive and works seamlessly on all devices (desktop, tablet, and mobile).

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **API**: [OMDB API](https://www.omdbapi.com/) for fetching movie data
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Roboto)
- **Dynamic Backgrounds**: Custom JavaScript for background slideshow

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Vijaykishore59/Movies-search.git
   cd Movies-search
>>>>>>> a295328fb9c4127b2b7e2a8ffcd3f6d733ceeb01
