# ACEest Fitness & Gym — DevOps CI/CD Project

A Flask-based REST API for ACEest Fitness & Gym with fully automated CI/CD pipelines using GitHub Actions, Jenkins, SonarCloud, Docker Hub, and Kubernetes (k3s on AWS EC2).

- **GitHub Repository:** https://github.com/gokulggowda-bits/aceest-fitness-devops.git
- **Docker Hub:** https://hub.docker.com/r/gokulggowdabits/aceest-fitness
- **SonarCloud:** https://sonarcloud.io/project/overview?id=gokulggowda-bits_aceest-fitness-devops
- **Jenkins:** http://3.6.72.107:8080
- **Live API:** http://3.6.72.107:30080

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Local Setup and Execution](#local-setup-and-execution)
4. [API Endpoints](#api-endpoints)
5. [Running Tests Manually](#running-tests-manually)
6. [Docker Usage](#docker-usage)
7. [Docker Hub](#docker-hub)
8. [SonarCloud Code Quality](#sonarcloud-code-quality)
9. [CI/CD Pipeline Architecture](#cicd-pipeline-architecture)
10. [GitHub Actions Workflow](#github-actions-workflow)
11. [Jenkins Pipeline](#jenkins-pipeline)
12. [Kubernetes Deployment on AWS EC2](#kubernetes-deployment-on-aws-ec2)
13. [Deployment Strategies](#deployment-strategies)
14. [Version Control Strategy](#version-control-strategy)
15. [Live Cluster Endpoints](#live-cluster-endpoints)
16. [Challenges and Mitigation](#challenges-and-mitigation)
17. [Deliverables Summary](#deliverables-summary)

---

## Project Overview

This project transitions the ACEest Fitness & Gym application from a Tkinter desktop app into a modern Flask REST API with a fully automated DevOps pipeline. The original codebase (versions 1.0 through 3.2.4) provided the business logic including fitness program definitions, calorie estimation, and BMI calculation, which were extracted and re-architected into stateless HTTP endpoints.

The CI/CD pipeline is fully automated — a single `git push` to the main branch triggers the entire workflow: linting, testing, code quality analysis, Docker image build and push, and Kubernetes deployment.

---

## Project Structure

```
aceest-fitness-devops/
├── app.py                          # Flask REST API application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
├── Jenkinsfile                     # Jenkins pipeline definition
├── sonar-project.properties        # SonarCloud configuration
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── tests/
│   ├── __init__.py
│   └── test_app.py                 # Pytest test suite
├── .github/
│   └── workflows/
│       └── main.yml                # GitHub Actions CI/CD pipeline
└── k8s/
    ├── deployment.yaml             # Base Kubernetes deployment + service
    ├── ab-testing.yaml             # A/B testing deployment
    ├── shadow-deployment.yaml      # Shadow deployment
    ├── rolling/
    │   └── deployment.yaml         # Rolling update deployment + service
    ├── blue-green/
    │   └── deploy.yaml             # Blue-Green deployment + service
    └── canary/
        └── deploy.yaml             # Canary deployment + service
```

---

## Local Setup and Execution

### Prerequisites

- Python 3.10 or higher
- pip
- Docker Desktop
- Git

### Steps

1. Clone the repository:

```bash
git clone https://github.com/gokulggowda-bits/aceest-fitness-devops.git
cd aceest-fitness-devops
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. The API will be available at http://localhost:5000

6. Verify by opening http://localhost:5000 in your browser. You should see:

```json
{
  "message": "Welcome to ACEest Fitness and Gym API",
  "status": "running"
}
```

---

## API Endpoints

| Method | Endpoint       | Description                         | Example Request Body               |
| ------ | -------------- | ----------------------------------- | ---------------------------------- |
| GET    | `/`            | Health check and API status         | —                                  |
| GET    | `/programs`    | List all available fitness programs | —                                  |
| GET    | `/program/<n>` | Get specific program details        | —                                  |
| POST   | `/calories`    | Calculate daily calorie target      | `{"weight": 80, "program": "fat"}` |
| POST   | `/bmi`         | Calculate BMI and category          | `{"weight": 70, "height": 175}`    |
| GET    | `/health`      | Health check with version info      | —                                  |

### Available Programs

- **Fat Loss (FL)** — Calorie factor: 22
- **Muscle Gain (MG)** — Calorie factor: 35
- **Beginner (BG)** — Calorie factor: 26

---

## Running Tests Manually

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with short traceback
pytest tests/ -v --tb=short
```

The test suite contains 17 test cases covering:

- Home endpoint (status code, JSON structure)
- Programs listing (status code, correct count)
- Individual program lookup (Fat Loss, Muscle Gain, Beginner, 404 for invalid)
- Calorie calculator (correct multiplication, invalid program error)
- BMI calculator (Normal, Overweight categories, missing data, negative input)
- Health check endpoint (status, version)
- Data integrity (all programs have required fields)

---

## Docker Usage

### Build the image locally

```bash
docker build -t gokulggowdabits/aceest-fitness:latest .
```

### Run the container

```bash
docker run -p 5000:5000 gokulggowdabits/aceest-fitness:latest
```

### Run tests inside the container

```bash
docker run --rm gokulggowdabits/aceest-fitness:latest pytest tests/ -v
```

### Dockerfile details

- **Base image:** python:3.11-slim (minimal footprint)
- **Layer caching:** requirements.txt installed before copying app code
- **No cache:** pip uses --no-cache-dir to keep image lean
- **Port:** 5000 exposed for the Flask application

---

## Docker Hub

All Docker images are versioned and published to Docker Hub.

- **Repository:** https://hub.docker.com/r/gokulggowdabits/aceest-fitness
- **Tags available:** v1.0, v2.0, latest, and build-number tags from Jenkins

### Pull and run from Docker Hub

```bash
docker pull gokulggowdabits/aceest-fitness:v2.0
docker run -p 5000:5000 gokulggowdabits/aceest-fitness:v2.0
```

---

## SonarCloud Code Quality

Static code analysis is automated via SonarCloud on every push to the main branch.

- **Dashboard:** https://sonarcloud.io/project/overview?id=gokulggowda-bits_aceest-fitness-devops
- **Metrics tracked:** Bugs, Vulnerabilities, Code Smells, Duplications
- **Integration:** Runs as a job in the GitHub Actions pipeline
- **Configuration:** Defined in `sonar-project.properties`

---

## CI/CD Pipeline Architecture

The pipeline is fully automated. A single `git push` to main triggers the entire workflow through two independent systems:

```
Developer pushes code to GitHub
        │
        ├──→ GitHub Actions (triggers immediately)
        │      ├── Job 1: Install Dependencies → Lint (flake8) → Test (Pytest)
        │      ├── Job 2: SonarCloud Code Quality Scan
        │      └── Job 3: Docker Build → Push to Docker Hub → Container Test
        │
        └──→ Jenkins (polls GitHub every 5 minutes)
               ├── Stage 1: Checkout code from GitHub
               ├── Stage 2: Build Docker image
               ├── Stage 3: Lint (flake8 inside container)
               ├── Stage 4: Test (Pytest inside container)
               ├── Stage 5: Push image to Docker Hub
               └── Stage 6: Deploy to Kubernetes (rolling update)
```

---

## GitHub Actions Workflow

**File:** `.github/workflows/main.yml`

Triggers on every push or pull request to the `main` branch. Consists of three sequential jobs:

### Job 1 — Build and Test

1. Checks out source code using actions/checkout@v4
2. Sets up Python 3.11 using actions/setup-python@v5
3. Installs all dependencies from requirements.txt
4. Runs flake8 linting with max line length of 120 characters
5. Executes the full Pytest suite in verbose mode

### Job 2 — SonarCloud Analysis (runs after Job 1 passes)

1. Checks out source code with full history (fetch-depth: 0)
2. Runs SonarCloud scan using SonarSource/sonarqube-scan-action@v4
3. Results are published to the SonarCloud dashboard

### Job 3 — Docker Build and Push (runs after Jobs 1 and 2 pass, only on main branch)

1. Checks out source code
2. Logs into Docker Hub using stored credentials
3. Builds Docker image tagged with commit SHA and latest
4. Pushes both tags to Docker Hub
5. Runs Pytest suite inside the container to verify containerized environment

---

## Jenkins Pipeline

**File:** `Jenkinsfile`

Jenkins is deployed on the same AWS EC2 instance as the Kubernetes cluster, running as a Docker container.

- **Jenkins URL:** http://3.6.72.107:8080
- **Pipeline:** aceest-fitness-pipeline
- **Trigger:** Polls GitHub SCM every 5 minutes

### Pipeline Stages

| Stage              | Description                                           |
| ------------------ | ----------------------------------------------------- |
| Checkout           | Clones latest code from GitHub main branch            |
| Build Docker Image | Builds Docker image with build number and latest tags |
| Lint               | Runs flake8 inside the container                      |
| Test               | Runs Pytest suite inside the container                |
| Push to Docker Hub | Authenticates and pushes images to Docker Hub         |
| Deploy to K8s      | Rolling update on the Kubernetes cluster              |

### Post Actions

- **On success:** Logs successful build number
- **On failure:** Automatically rolls back the Kubernetes deployment to the previous version

---

## Kubernetes Deployment on AWS EC2

### Infrastructure Setup

- **Cloud Provider:** AWS (ap-south-1 / Mumbai region)
- **Instance Type:** t2.small (2 vCPU, 2 GB RAM + 2 GB swap)
- **OS:** Ubuntu Server 24.04 LTS
- **Kubernetes:** k3s (lightweight Kubernetes distribution)
- **Elastic IP:** 3.6.72.107

### Setup Steps Executed

1. Launched EC2 instance with security group allowing ports 22, 5000, 8080, 9000, 30080-30086
2. Allocated and associated an Elastic IP for a permanent public address
3. Added 2GB swap space to supplement the 2GB RAM
4. Installed Docker and logged into Docker Hub
5. Pulled versioned images (v1.0, v2.0) from Docker Hub
6. Installed k3s (lightweight Kubernetes) and configured kubectl
7. Installed Jenkins as a Docker container with Docker socket and kubectl access
8. Created Kubernetes deployments for all strategies using YAML manifests
9. Configured Jenkins pipeline to poll GitHub and auto-deploy on changes

---

## Deployment Strategies

All deployment strategies are implemented and running on the Kubernetes cluster.

### 1. Base Deployment (Port 30080)

Standard Kubernetes deployment with replicas and a NodePort service.

```bash
kubectl apply -f k8s/deployment.yaml
```

### 2. Rolling Update (Port 30081)

Zero-downtime update strategy. New pods are created before old ones are terminated.

```bash
# Deploy v1.0
kubectl apply -f k8s/rolling/deployment.yaml

# Trigger rolling update to v2.0
kubectl set image deployment/aceest-rolling aceest-fitness=gokulggowdabits/aceest-fitness:v2.0

# Monitor rollout
kubectl rollout status deployment/aceest-rolling

# Rollback if needed
kubectl rollout undo deployment/aceest-rolling
```

### 3. Blue-Green Deployment (Port 30082)

Two identical environments (Blue = v1.0, Green = v2.0). Traffic is switched instantly by updating the service selector.

```bash
# Deploy both versions
kubectl apply -f k8s/blue-green/deploy.yaml

# Switch from Blue (v1.0) to Green (v2.0)
kubectl patch service aceest-bluegreen-service -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback to Blue (v1.0)
kubectl patch service aceest-bluegreen-service -p '{"spec":{"selector":{"version":"blue"}}}'
```

### 4. Canary Deployment (Port 30083)

Gradual rollout where a small percentage of traffic goes to the new version. Stable pods run v1.0, canary pod runs v2.0.

```bash
# Deploy stable (2 pods) + canary (1 pod)
kubectl apply -f k8s/canary/deploy.yaml

# ~67% traffic goes to v1.0, ~33% to v2.0

# Promote canary to full production
kubectl scale deployment aceest-canary --replicas=2
kubectl scale deployment aceest-stable --replicas=0

# Rollback
kubectl scale deployment aceest-canary --replicas=0
kubectl scale deployment aceest-stable --replicas=2
```

### 5. A/B Testing (Ports 30084 and 30085)

Two versions served on separate endpoints for user segment testing.

```bash
kubectl apply -f k8s/ab-testing.yaml

# Version A (v1.0): http://3.6.72.107:30084
# Version B (v2.0): http://3.6.72.107:30085
```

### 6. Shadow Deployment (Port 30086)

Production pods serve real user traffic. Shadow pods run the new version silently for monitoring without impacting users.

```bash
kubectl apply -f k8s/shadow-deployment.yaml

# Only production (v1.0) serves traffic on port 30086
# Shadow (v2.0) runs in parallel for testing
```

---

## Version Control Strategy

### Branching

- **main** — Production-ready code, protected by CI/CD gates
- **develop** — Feature development branch, merged to main after validation

### Tagging

| Tag  | Description                                          |
| ---- | ---------------------------------------------------- |
| v1.0 | Base Flask API with programs, calories, and BMI      |
| v2.0 | Added health check endpoint with version info        |
| v2.1 | Fully automated CI/CD with K8s deployment strategies |

### Commit Convention

Commits follow conventional commit standards with descriptive prefixes:

- `feat:` — New features
- `fix:` — Bug fixes
- `test:` — Test additions or updates
- `ci:` — CI/CD pipeline changes
- `infra:` — Infrastructure and deployment changes
- `docs:` — Documentation updates

---

## Live Cluster Endpoints

All endpoints are publicly accessible:

| Strategy        | URL                     | Port  | Status |
| --------------- | ----------------------- | ----- | ------ |
| Base Deployment | http://3.6.72.107:30080 | 30080 | Live   |
| Rolling Update  | http://3.6.72.107:30081 | 30081 | Live   |
| Blue-Green      | http://3.6.72.107:30082 | 30082 | Live   |
| Canary          | http://3.6.72.107:30083 | 30083 | Live   |
| A/B Testing (A) | http://3.6.72.107:30084 | 30084 | Live   |
| A/B Testing (B) | http://3.6.72.107:30085 | 30085 | Live   |
| Shadow          | http://3.6.72.107:30086 | 30086 | Live   |
| Jenkins         | http://3.6.72.107:8080  | 8080  | Live   |

---

## Challenges and Mitigation

| Challenge                                                                        | Mitigation                                                                                                               |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| t2.micro had insufficient memory (1GB) for running k3s + Jenkins + multiple pods | Upgraded to t2.small (2GB) and added 2GB swap space for a total of 4GB usable memory                                     |
| Jenkins GPG key expired during apt installation on Ubuntu                        | Switched to running Jenkins as a Docker container, which avoids OS package dependency issues                             |
| Jenkins container could not reach k3s API on 127.0.0.1                           | Updated kubeconfig inside the Jenkins container to use the EC2 instance's private IP (172.31.32.34) instead of localhost |
| SonarCloud scan failed due to Automatic Analysis conflict                        | Disabled Automatic Analysis in SonarCloud settings, allowing CI-based analysis via GitHub Actions                        |
| flake8 linting errors (blank line spacing) blocking pipeline                     | Fixed PEP 8 spacing issues in app.py to comply with flake8 standards                                                     |
| Docker Hub push failed with "access denied"                                      | Generated a Personal Access Token on Docker Hub and stored it as a GitHub Actions secret                                 |
| EC2 public IP changed after instance stop/start                                  | Allocated and associated an AWS Elastic IP for a permanent public address                                                |

---

## Technologies Used

| Category           | Tool / Service       |
| ------------------ | -------------------- |
| Web Framework      | Flask                |
| Testing            | Pytest               |
| Linting            | flake8               |
| Code Quality       | SonarCloud           |
| Containerization   | Docker               |
| Container Registry | Docker Hub           |
| CI/CD (Pipeline 1) | GitHub Actions       |
| CI/CD (Pipeline 2) | Jenkins              |
| Orchestration      | Kubernetes (k3s)     |
| Cloud Provider     | AWS EC2 (ap-south-1) |
| Version Control    | Git / GitHub         |

---

## Deliverables Summary

| #   | Deliverable               | Location / Link                                                                  | Status             |
| --- | ------------------------- | -------------------------------------------------------------------------------- | ------------------ |
| 1   | Flask Application         | `app.py`, `requirements.txt` in repo                                             | Complete           |
| 2   | Jenkinsfile               | `Jenkinsfile` in repo root                                                       | Complete           |
| 3   | Dockerfile                | `Dockerfile` in repo root                                                        | Complete           |
| 4   | Kubernetes YAML Manifests | `k8s/` folder with all deployment strategy files                                 | Complete           |
| 5   | Pytest Test Cases         | `tests/test_app.py` (17 tests, all passing)                                      | Complete           |
| 6   | SonarCloud Report         | https://sonarcloud.io/project/overview?id=gokulggowda-bits_aceest-fitness-devops | Complete           |
| 7   | GitHub Repository         | https://github.com/gokulggowda-bits/aceest-fitness-devops.git                    | Public             |
| 8   | Docker Hub Images         | https://hub.docker.com/r/gokulggowdabits/aceest-fitness                          | v1.0, v2.0, latest |
| 9   | Jenkins CI/CD             | http://3.6.72.107:8080                                                           | Running            |
| 10  | Live Cluster Endpoints    | http://3.6.72.107:30080 through :30086                                           | All Live           |
| 11  | Deployment Strategies     | Rolling, Blue-Green, Canary, A/B Testing, Shadow — all implemented               | Complete           |
