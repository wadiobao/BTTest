# Demo FastAPI Application

## Setup

1. Clone repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create .env file with following content:
```env
MYSQL_ROOT_PASSWORD=root123
MYSQL_DATABASE=quan_li_sinh_vien
DOCKER_USERNAME=your-dockerhub-username
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

4. Access the application:
- API Documentation: http://localhost:8000/docs
- API Base URL: http://localhost:8000

## Features
- FastAPI backend
- MySQL database
- Docker containerization
- Swagger UI documentation

## API Endpoints
- GET /sinhvien/hienthi/tatca
- GET /khoa/hienthi/tatca
- GET /lop/hienthi/tatca
- And more... (see Swagger UI for full documentation) 