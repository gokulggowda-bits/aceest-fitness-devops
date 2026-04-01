# ACEest Fitness & Gym — DevOps CI/CD Project

A Flask-based REST API for ACEest Fitness & Gym with full CI/CD automation
using GitHub Actions and Jenkins.

## Project Structure

aceest-fitness-devops/
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── Dockerfile # Container configuration
├── tests/
│ └── test_app.py # Pytest test suite
├── .github/
│ └── workflows/
│ └── main.yml # GitHub Actions pipeline
└── README.md # This file

## Local Setup and Execution

### Prerequisites

- Python 3.10+
- pip
- Docker Desktop (for containerization)
- Git

### Steps

1. Clone the repository:

```bash
   git clone https://github.com/YOUR_USERNAME/aceest-fitness-devops.git
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

The API will be available at http://localhost:5000

### API Endpoints

| Method | Endpoint        | Description               |
| ------ | --------------- | ------------------------- |
| GET    | /               | Health check              |
| GET    | /programs       | List all fitness programs |
| GET    | /program/<name> | Get program details       |
| POST   | /calories       | Calculate daily calories  |
| POST   | /bmi            | Calculate BMI             |

## Running Tests Manually

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage (install pytest-cov first)
pytest tests/ -v --tb=short
```

## Docker Usage

```bash
# Build the image
docker build -t aceest-fitness .

# Run the container
docker run -p 5000:5000 aceest-fitness

# Run tests inside the container
docker run aceest-fitness pytest tests/ -v
```

## CI/CD Pipeline Overview

### GitHub Actions (.github/workflows/main.yml)

The automated pipeline triggers on every **push** or **pull request** to the
`main` branch. It runs two sequential jobs:

1. **Build & Test Job:**
   - Checks out the source code
   - Sets up Python 3.11
   - Installs all dependencies from requirements.txt
   - Runs flake8 linting to catch syntax and style errors
   - Executes the full Pytest suite

2. **Docker Build Job** (runs only if Job 1 passes):
   - Builds the Docker image from the Dockerfile
   - Runs the Pytest suite inside the container to verify
     the containerized environment works correctly

### Jenkins Integration

Jenkins serves as a secondary BUILD and quality gate:

1. A Jenkins Pipeline project is configured to pull code from the
   GitHub repository.
2. The pipeline stages are:
   - **Checkout:** Clones the latest code from the main branch
   - **Install:** Installs Python dependencies
   - **Lint:** Runs flake8 for code quality checks
   - **Test:** Executes Pytest to validate all endpoints
   - **Docker Build:** Builds the Docker image in the Jenkins environment
3. This provides an independent validation layer separate from
   GitHub Actions, ensuring the code compiles and integrates
   correctly in a controlled build server.

## Technologies Used

- **Flask** — Lightweight Python web framework
- **Pytest** — Python testing framework
- **Docker** — Application containerization
- **GitHub Actions** — CI/CD pipeline automation
- **Jenkins** — Secondary build server and quality gate
- **flake8** — Python linting and style enforcement
