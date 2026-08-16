# SoleStyle — E-commerce (SoleStyle)

A lightweight e-commerce sample project (backend + static frontend) for a shoes/store called "SoleStyle". This repository contains a FastAPI backend that talks to MongoDB and a simple static HTML/CSS/JS frontend.

---

## Project structure

- backend/ — FastAPI app, database access, Pydantic models, routes, and seed script
- frontend/ — Static site (HTML/CSS/JS) for browsing, cart, checkout UI
- requirements.txt — top-level requirements (note: backend has its own requirements)


## Tech stack

- Backend: FastAPI, Uvicorn
- Database: MongoDB (Motor async driver)
- Auth & security: JWT (python-jose), bcrypt
- Frontend: Static HTML/CSS/vanilla JS (files in `frontend/`)


## Features

- Product listing with search, filters, paging and sort
- Product details, reviews
- User authentication (JWT)
- Cart, wishlist and orders endpoints
- Database indexes for search and performance
- Seed script to populate sample products and users


## Prerequisites

- Python 3.11+ (project used pydantic v2 and recent libs)
- MongoDB instance (local or hosted)
- (Optional) Razorpay keys for payments if you want to test payments
- Node/npm (optional) or any static file server to serve `frontend/`


## Backend — Quick start

1. Create a Python virtual environment and activate it

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # PowerShell
   .\.venv\Scripts\activate.bat   # cmd.exe

2. Install backend dependencies

   pip install -r backend\requirements.txt

3. Create a `.env` file in `backend/` (or set environment variables) with at least:

   MONGODB_URL=mongodb://localhost:27017
   JWT_SECRET=your_long_random_secret
   RAZORPAY_KEY_ID=your_razorpay_key_id
   RAZORPAY_KEY_SECRET=your_razorpay_key_secret
   # FRONTEND_URL is optional (used for CORS)

4. Run the application (from repository root):

   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

   - API docs are available at: http://127.0.0.1:8000/docs
   - Health check: http://127.0.0.1:8000/health


## Seeding sample data

The project includes `backend/seed.py` that inserts sample products and example users into the database for local testing.

Run it with:

   python backend\seed.py

(note: run from repository root; ensure `MONGODB_URL` is set so the script can connect)


## Frontend — Quick start

The frontend is static files in `frontend/`. To view locally:

- Option A — Use Python's simple server (from `frontend` folder):

  cd frontend
  python -m http.server 5500
  # then open http://127.0.0.1:5500

- Option B — Open `frontend/index.html` directly in the browser (some features that call the API or require CORS may need a local server)

The frontend uses `js/api.js` to call the backend API at `/api/*`. By default CORS in the backend allows `http://localhost:5500` and the Netlify URL configured in settings.


## Important environment variables

(Place these in `backend/.env` or export in your environment)

- MONGODB_URL — MongoDB connection string
- JWT_SECRET — secret used to sign JWT tokens
- RAZORPAY_KEY_ID — (optional) for payment integration
- RAZORPAY_KEY_SECRET — (optional)
- FRONTEND_URL — allowed origin for CORS (defaults to Netlify URL in config)


## API overview (selected endpoints)

- GET /api/products — list products (query params: search, category, brand, page, limit, sort_by)
- GET /api/products/featured — featured products
- GET /api/products/new-arrivals — new arrivals
- GET /api/products/{id} — product detail
- POST /api/products — create product (protected)
- PUT /api/products/{id} — update product (protected)
- DELETE /api/products/{id} — delete product (protected)
- POST /api/products/{id}/reviews — add review (protected)

- Auth, cart, wishlist, orders routes are mounted under `/api/` as well (see `backend/routes/` for details).

Use the interactive docs at `/docs` to explore request/response models.


## Development notes

- Database indexes are created on startup via `create_indexes()` in `backend/database.py`.
- Password hashing uses bcrypt wrappers in `backend/utils/security.py`.
- Pydantic models (v2-style BaseModel) define request/response shapes in `backend/models/`.
- The seed script provides a large sample dataset; inspect `backend/seed.py` for contents.


## Troubleshooting

- If models fail to import when running a script, ensure current working directory is repository root (so `backend` package imports resolve).
- If CORS blocks frontend requests, confirm `FRONTEND_URL` or your localhost origin is allowed in `backend/config.py` (or `.env`).
- Ensure MongoDB is reachable at `MONGODB_URL`.


## Contributing

Contributions welcome. Open issues or PRs with focused changes. Keep changes small and test locally.


## License

This repository does not include an explicit license file. Add a LICENSE file if you intend to publish with a specific license.


## Contact / Authors

Project: SoleStyle (example/sample project)

---

Generated README based on the repository files found in this workspace. Update any environment values, deployment instructions, or payment integration details before deploying to production.
