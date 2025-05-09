# FastAPI_newsapi_OAuth2.0
microservice API designed with FastAPI where newsapi integreted with OAuth2.0 Authentication

A production-ready FastAPI application that fetches and manages news articles using the [NewsAPI](https://newsapi.org). The application supports OAuth2.0 client credentials authentication and provides multiple endpoints for interacting with news data.

---

## Project Description

This FastAPI project integrates with the NewsAPI to:

- Authenticate via OAuth2 client credentials flow
- Fetch global news with pagination support
- Save top 3 unique latest headlines from NewsAPI by country and/or source
- Get news headlines filtered by country or source
- Secure all endpoints with bearer token authentication

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/mdparvex/FastAPI_newsapi_OAuth2.0.git
cd FastAPI_newsapi_OAuth2.0
```

### 2. Create a `.env` File

```env
NEWS_API_KEY=your_news_api_key
CLIENT_ID=testuser
CLIENT_SECRET=testuser
SECRET_KEY=your_secret_key
ALGORITHM=HS256
BASE_URL=https://newsapi.org/v2

POSTGRES_DB=newsdb
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DATABASE_URL=postgresql://user:password@db:5432/newsdb
```


## Setup locally
Create a virtual environment
```bash
python -m virtualenv <environment_name>
```
Activate the virtual environment
```bash
cd <environment_name>\Scripts
activate
```
install requirements.txt
```bash
pip install -r requirements.txt
```
## How to Run the Server
Go to the project root directory and run
```bash
uvicorn app.main:app --reload
```

Access it at: http://localhost:8000/docs

## How to Run Tests

### Run All Tests with Pytest:
From the root directory where main.py is under /app
```bash
pytest tests
```
## How to Use Docker


### Docker Compose Includes:

- `web` - FastAPI container
- `db` - PostgreSQL container with volume for persistence

---
### Run with Docker Compose

```bash
docker-compose up --build
```

Then open: http://localhost:8000/docs

---

## How to Generate Access Tokens

### Step 1: Call `/token` with Basic Auth

**POST /token**

```http
Authorization: Basic base64(client_id:client_secret)
```


```http
http://localhost:8000/token
```
```json
Headers:{
      headers: "Authorization: Basic dGVzdHVzZXI6dGVzdHVzZXI="
}
```

Returns:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Step 2: Use Token in Secured Endpoints

```http
Authorization: Bearer <access_token>
```

Use client_id:testuser (testing purpose for me defined in .env file), client_secret:testuser - in Swagger UI Authorize dialog.

---

## API Endpoints and Usage

### 1. `GET /news`

**Fetch paginated news from NewsAPI /everything**

```http
/news?skip=0&limit=10&query=technology
```

Returns:

```json
{
  "page": 1,
  "pageSize": 10,
  "totalResults": 134,
  "next": "/news?skip=10&limit=10&query=news",
  "previous": null,
  "articles": [ ... ]
}
```

---

### 2. `POST /news/save-latest`

**Save top 3 latest news (must be unique by URL)**

```json
POST /news/save-latest
{
  "country_code": "us",
  "source_id": "cnn"
}
```

Returns:

```json
{
  "message": "Saved top 3 latest news"
}
```

---

### 3. `GET /news/headlines/country/{country_code}`

**Get latest headlines by country**

```http
/news/headlines/country/us
```

Returns:

```json
{
  "articles": [ ... ]
}
```

---

### 4. `GET /news/headlines/source/{source_id}`

**Get headlines from a specific source**

```http
/news/headlines/source/cnn
```

Returns:

```json
{
  "articles": [ ... ]
}
```

---

### 5. `GET /news/headlines/filter`

**Filter headlines by country and/or source**

```http
/news/headlines/filter?country=us&source=cnn
```

- Fetches headlines by country and filters results by source from the API response.

Returns:

```json
{
  "totalResults": 2,
  "articles": [
    {
      "source": { "id": "cnn" },
      ...
    }
  ]
}
```

---

## Final Notes

- Ensure your NewsAPI key is active and has access to `everything` endpoint
- Ensure PostgreSQL container is reachable with proper `.env` configuration
- Ensure to use a proper database connection for Locan and Docker in `.env` configuration
- Use Swagger UI at `/docs` to interact with all secured endpoints

