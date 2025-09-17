# FastAPI Referral System API

## How to Set Up and Run the Project

### Prerequisites
- Python 3.12.
- pip (included with Python).
- Docker and Docker Compose (optional, for PostgreSQL setup).
- Git (to clone the repository).

### Local Development (SQLite)
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd referral_api
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate and Apply Migrations**:
   ```bash
   alembic revision --autogenerate -m "initial"
   alembic upgrade head
   ```

5. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Access the API at `http://127.0.0.1:8000`.

### Docker Setup (PostgreSQL)
1. **Copy Environment File**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if needed (e.g., update `DATABASE_URL` for PostgreSQL).

2. **Build and Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Apply Migrations**:
   Inside the app container:
   ```bash
   docker-compose exec app alembic revision --autogenerate -m "initial"
   docker-compose exec app alembic upgrade head
   ```

4. **Access the API**:
   Open `http://localhost:8000`.

5. **Access the API Documentation**:
   Open `http://localhost:8000/docs`.
