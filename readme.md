# Hash Service - Flask Application with OpenTelemetry

## Overview
The **Hash Service** is a simple Flask-based microservice that computes the SHA-256 hash of a given input string. It includes OpenTelemetry tracing for monitoring and observability and is containerized using Docker. The application is deployed using GitHub Actions with automatic builds and pushes to Docker Hub.

## Features
- Computes SHA-256 hashes for input strings.
- Implements OpenTelemetry tracing with Jaeger Exporter.
- Provides a health check endpoint.
- Uses Gunicorn for production deployment.
- Dockerized with multi-stage builds for optimized images.
- CI/CD pipeline for automated builds and Docker image push.
- We use a Helm chart to deploy the application, which simplifies Kubernetes deployment and management.
---

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Docker Deployment](#docker-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Configuration](#configuration)
7. [Dockerfile Explanation](#dockerfile-explanation)
8. [Code Explanation](#code-explanation)
9. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.9+
- Flask
- Docker
- Jaeger (for tracing)
- Gunicorn

### Install Dependencies
```sh
pip install -r requirements.txt
```

---

## Usage

### Running the Application Locally
```sh
python hash_service.py
```

By default, the application runs on **port 8080**.

---

## API Endpoints

### 1. **Generate SHA-256 Hash**
- **URL**: `/hash`
- **Method**: `POST`
- **Description**: Takes a string as input and returns its SHA-256 hash.
- **Request Body**:
  ```text
  "Hello, World"
  ```
- **Response**:
  ```json
  "03675ac53ff9cd1535ccc7dfcdfa2c458c5218371f418dc136f2d19ac1fbe8a5"
  ```


### 2. **Health Check**
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Checks if the service is running.
- **Response**:
  ```json
  {"status": "healthy"}
  ```

---

## Docker Deployment

### **Building and Running the Container**
```sh
docker build -t hash-service .
docker run -p 8080:8080 hash-service
```

### **Accessing the API Inside Docker**
```sh
curl -X POST http://localhost:8080/hash -d "Hello, World!"
```

---

## CI/CD Pipeline
This project includes a GitHub Actions workflow to **build and push** the Docker image to Docker Hub on each push to the `main` branch.

### **Pipeline Workflow**
- **Checkout Code**: Fetches the latest changes.
- **Set Up Docker Buildx**: Enables multi-platform builds.
- **Login to Docker Hub**: Authenticates using stored secrets.
- **Build and Push Docker Image**: Builds and pushes `ahmadkurdi/hash:latest` to Docker Hub.

### **Triggering the Workflow**
The pipeline runs automatically on a `git push` to `main`, or manually via the GitHub UI.

---

## Configuration
### **Environment Variables**
| Variable | Description |
|----------|-------------|
| `OTEL_EXPORTER_JAEGER_ENDPOINT` | Jaeger exporter URL (default: `http://jaeger-collector.jaeger.svc.cluster.local:14268/api/traces`) |

---

## Dockerfile Explanation
The Dockerfile is designed to optimize image size and security using a multi-stage build:

1. **Use a builder stage (`python:3.9-slim`)**:
   - This stage installs necessary dependencies without bloating the final image.
   - The `--no-cache-dir` flag ensures a smaller image by avoiding unnecessary cache files.

2. **Create a runtime image (`python:3.9-slim`)**:
   - Uses a minimal Python image to reduce attack surface and improve performance.
   - Copies installed dependencies from the builder stage to avoid unnecessary installations.

3. **Use a non-root user (`appuser`)**:
   - Improves security by preventing privileged access within the container.

4. **Expose port 8080**:
   - Ensures the application is accessible on the correct port.

5. **Use Gunicorn for production**:
   - Gunicorn improves performance and handles multiple concurrent requests efficiently.

---

## Code Explanation
### **hash_service.py**
- **Logging Setup**:
  - Enables debug logging to assist with troubleshooting.

- **OpenTelemetry Tracing**:
  - Sets up `JaegerExporter` to send traces to a Jaeger instance.
  - Uses `BatchSpanProcessor` to optimize trace exports.
  - Instruments Flask for automatic request tracing.

- **Hashing Function (`/hash` endpoint)**:
  - Receives raw input from a `POST` request.
  - Computes SHA-256 hash using Python's `hashlib` module.
  - Records request attributes in OpenTelemetry spans.
  - Returns the computed hash.

- **Health Check Endpoint (`/health`)**:
  - Provides a simple status check to confirm the service is running.

- **Gunicorn-based Deployment**:
  - The app runs on `0.0.0.0:8080` to be accessible inside Docker.




