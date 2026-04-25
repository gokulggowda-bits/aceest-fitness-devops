import pytest
from app import app, PROGRAMS


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------- HOME ENDPOINT ----------

def test_home_status_code(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_home_message(client):
    resp = client.get("/")
    data = resp.get_json()
    assert "ACEest" in data["message"]
    assert data["status"] == "running"


# ---------- PROGRAMS ENDPOINT ----------

def test_get_programs_status(client):
    resp = client.get("/programs")
    assert resp.status_code == 200


def test_get_programs_count(client):
    resp = client.get("/programs")
    data = resp.get_json()
    assert len(data["programs"]) == 3


# ---------- SINGLE PROGRAM ENDPOINT ----------

def test_get_program_fat_loss(client):
    resp = client.get("/program/fat")
    assert resp.status_code == 200
    assert "Fat Loss" in resp.get_json()["program"]


def test_get_program_muscle_gain(client):
    resp = client.get("/program/muscle")
    assert resp.status_code == 200
    assert "Muscle Gain" in resp.get_json()["program"]


def test_get_program_beginner(client):
    resp = client.get("/program/beginner")
    assert resp.status_code == 200
    assert "Beginner" in resp.get_json()["program"]


def test_get_program_not_found(client):
    resp = client.get("/program/nonexistent")
    assert resp.status_code == 404


# ---------- CALORIE CALCULATOR ENDPOINT ----------

def test_calories_fat_loss(client):
    resp = client.post("/calories", json={"weight": 80, "program": "fat"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["daily_calories"] == 80 * 22  # factor = 22


def test_calories_muscle_gain(client):
    resp = client.post("/calories", json={"weight": 70, "program": "muscle"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["daily_calories"] == 70 * 35  # factor = 35


def test_calories_invalid_program(client):
    resp = client.post("/calories", json={"weight": 80, "program": "xyz"})
    assert resp.status_code == 400


# ---------- BMI ENDPOINT ----------

def test_bmi_normal(client):
    # 70kg, 175cm -> BMI ~22.9 -> Normal
    resp = client.post("/bmi", json={"weight": 70, "height": 175})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["category"] == "Normal"
    assert data["bmi"] > 0


def test_bmi_overweight(client):
    # 90kg, 170cm -> BMI ~31.1 -> Obese
    resp = client.post("/bmi", json={"weight": 90, "height": 170})
    assert resp.status_code == 200


def test_bmi_missing_data(client):
    resp = client.post("/bmi", json={"weight": 0, "height": 175})
    assert resp.status_code == 400


def test_bmi_negative_height(client):
    resp = client.post("/bmi", json={"weight": 70, "height": -10})
    assert resp.status_code == 400


# ---------- DATA INTEGRITY ----------

def test_all_programs_have_required_fields():
    for name, details in PROGRAMS.items():
        assert "workout" in details, f"{name} missing workout"
        assert "diet" in details, f"{name} missing diet"
        assert "calorie_factor" in details, f"{name} missing calorie_factor"
        assert details["calorie_factor"] > 0, f"{name} has invalid calorie_factor"
        
#---------- HEALTH CHECK ENDPOINT ----------
def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0"