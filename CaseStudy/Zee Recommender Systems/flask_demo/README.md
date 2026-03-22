# Flask Demo - Docker Setup

## Build and Run with Docker

### Build the Docker image:
```bash
docker build -t flask-demo-app .
```

### Run the container:
```bash
docker run -p 5000:5000 flask-demo-app
```

### Access the app:
Open http://localhost:5000 in your browser

### Run in detached mode:
```bash
docker run -d -p 5000:5000 --name flask-demo flask-demo-app
```

### Stop the container:
```bash
docker stop flask-demo
```

### Remove the container:
```bash
docker rm flask-demo
```

### View logs:
```bash
docker logs flask-demo
```

## Docker Compose (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

Run with:
```bash
docker-compose up
```
