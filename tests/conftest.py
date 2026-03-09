import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Initial state of activities for resetting between tests
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis training and friendly tournaments",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu", "sarah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and visual arts exploration",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn instruments and perform in concerts",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["benjamin@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore scientific experiments and discoveries",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Fixture to provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Fixture to reset the activities dict to initial state before each test."""
    # Deep copy the initial activities to reset
    import copy
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))