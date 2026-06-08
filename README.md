# PropertyNest

A full-stack property rental management platform built for the **PACE 2026 Hackathon (Track 1)**. PropertyNest allows tenants to browse and apply for rental properties, landlords to list and manage their properties, and administrators to oversee the entire platform.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + React Router |
| Backend | FastAPI (Python 3.12) |
| Relational DB | PostgreSQL 15 |
| Document DB | MongoDB 6 (via Beanie ODM) |
| Reverse Proxy | Nginx |
| CI/CD | GitHub Actions |
| Auth | JWT (PyJWT + bcrypt) |

## Folder Structure

```
property_nest/
├── app/                        # FastAPI backend
│   ├── main.py                 # App entrypoint + lifespan
│   ├── auth.py                 # JWT helpers (hash, verify, token)
│   ├── database/
│   │   └── connection.py       # PostgreSQL + MongoDB connections
│   ├── models/
│   │   ├── pg_models.py        # SQLAlchemy table definitions
│   │   └── mongo_models.py     # Beanie document models
│   ├── schemas/                # Pydantic request/response models
│   ├── routes/                 # FastAPI routers (7 route files)
│   └── services/               # Business logic layer
├── frontend/                   # React frontend
│   └── src/
│       ├── pages/              # 8 page components
│       ├── components/         # Reusable UI components
│       ├── services/api.js     # All API calls in one place
│       └── hooks/              # AuthContext provider
├── tests/                      # pytest async tests
├── alembic/                    # Database migrations
├── scripts/                    # Seed data + verification
├── .github/workflows/ci.yml   # GitHub Actions CI pipeline
├── setup.sh                    # Ubuntu setup script
├── requirements.txt            # Python dependencies
└── nginx.conf                  # Nginx reverse proxy config
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- MongoDB 6+ (or a MongoDB Atlas cluster)
- Nginx (for production)

### 1. Clone the Repository

```bash
git clone https://github.com/sriram53-codincity/PropertyNest.git
cd PropertyNest
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# PostgreSQL
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=homelease
PG_USER=postgres
PG_PASSWORD=your_password

# MongoDB
MONGO_URL=mongodb://localhost:27017/homelease
MONGO_DB=homelease

# JWT Secret (min 32 characters recommended)
SECRET_KEY=your-secret-key-at-least-32-chars-long

# Upload directory
UPLOAD_DIR=uploads
```

### 4. Create the PostgreSQL Database

```bash
createdb homelease
```

### 5. Start the Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` and Swagger docs at `http://localhost:8000/docs`.

### 6. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 7. Run Tests

```bash
pytest tests/
```

## Environment Variables Reference

| Variable | Description | Example |
|---|---|---|
| `PG_HOST` | PostgreSQL host | `localhost` |
| `PG_PORT` | PostgreSQL port | `5432` |
| `PG_DATABASE` | PostgreSQL database name | `homelease` |
| `PG_USER` | PostgreSQL username | `postgres` |
| `PG_PASSWORD` | PostgreSQL password | `your_password` |
| `MONGO_URL` | MongoDB connection string | `mongodb://localhost:27017/homelease` |
| `MONGO_DB` | MongoDB database name | `homelease` |
| `SECRET_KEY` | JWT signing key (min 32 chars) | `my-secret-key-abc123...` |
| `UPLOAD_DIR` | Directory for uploaded files | `uploads` |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user profile |
| GET | `/api/properties/` | List/search properties (with filters) |
| POST | `/api/properties/` | Create a new property |
| GET | `/api/properties/{id}` | Get property details |
| PUT | `/api/properties/{id}` | Update a property |
| DELETE | `/api/properties/{id}` | Delete a property |
| POST | `/api/applications/` | Submit a rental application |
| GET | `/api/applications/` | List applications |
| PUT | `/api/applications/{id}/status` | Approve/Reject application |
| POST | `/api/seller-requests/` | Submit a seller request |
| GET | `/api/seller-requests/` | List seller requests |
| PUT | `/api/seller-requests/{id}/status` | Approve/Reject seller request |
| GET | `/api/leases/` | List leases |
| POST | `/api/maintenance/` | Create maintenance request |
| GET | `/api/maintenance/` | List maintenance requests |
| POST | `/api/appointments/` | Book an appointment |
| GET | `/api/appointments/` | List appointments |
| PUT | `/api/appointments/{id}/status` | Confirm/Reject appointment |

## Quick Setup (Ubuntu)

```bash
chmod +x setup.sh
./setup.sh
```

## License

Built for PACE 2026 Hackathon — Track 1 Team Project.
