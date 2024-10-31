import pytest
from unittest.mock import MagicMock
from bs4 import BeautifulSoup

def test_program_route_user_not_logged_in(client):
    response = client.get("/program")
    assert response.status_code == 302  # Redirect status
    assert response.location.endswith("/dashboard")  # Redirects to the dashboard

def test_enroll_invalid_program_id(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    response = client.post("/enroll", data={
        "exercise": "example_exercise",
        "program_id": "invalid_id"  # Non-existent ObjectId
    })
    # error handling
    assert response.status_code == 302  # Redirect status
    assert response.location.endswith("/dashboard")  # Redirects to the dashboard

def test_cancel_enrollment_not_enrolled(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    response = client.post("/cancel_enrollment", data={
        "exercise": "example_exercise",
        "program_id": "60d5ec4a2d3b3c0b94c4b5d7"  # Assume user is not enrolled in this program
    })
    # error handling
    assert response.status_code == 302  # Redirect status
    assert response.location.endswith("/dashboard")  # Redirects to the dashboard

def test_my_programs_user_not_logged_in(client):
    response = client.get("/my_programs")
    assert response.status_code == 302  # Redirect status
    assert response.location.endswith("/dashboard")  # Redirects to the dashboard

def test_program_route_non_existent_exercise(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    response = client.get("/program?exercise=nonexistent_exercise")
    # Assumes error handling if exercise not found
    assert response.status_code == 302  # Redirect status
    assert response.location.endswith("/dashboard")  # Redirects to the dashboard

def test_program_route_with_valid_exercise(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    with client.application.app_context():
        # Insert a mock exercise and program plan into the database
        client.application.mongo.db.your_exercise_collection.insert_one({
            "email": "email",
            "exercise_id": 2,
            "image": "example_exercise.jpeg",
            "video_link": "link",
            "name": "Example Exercise",
            "intro": "Example Exercise intro",
            "description": "Example exercise description",
            "plan_image": "example_exercise.jpeg",
            "href": "example_exercise"
        })
        client.application.mongo.db.program_plan.insert_one({
            "title": "Test Program",
            "exercise": "example_exercise",
            "month": "Oct",
            "dates": ["2024-10-27", "2024-10-28", "2024-10-29", "2024-10-30", "2024-10-31", "2024-11-01", "2024-11-02"]
        })
    response = client.get("/program?exercise=example_exercise")
    assert b"Test Program" in response.data

def test_enroll_in_program_successfully(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    with client.application.app_context():
        # Insert a mock program plan
        client.application.mongo.db.your_exercise_collection.insert_one({
            "email": "email",
            "exercise_id": 2,
            "image": "example_exercise.jpeg",
            "video_link": "link",
            "name": "Example Exercise",
            "intro": "Example Exercise intro",
            "description": "Example exercise description",
            "plan_image": "example_exercise.jpeg",
            "href": "example_exercise"
        })
        program_id = client.application.mongo.db.program_plan.insert_one({
            "title": "Test Program",
            "exercise": "example_exercise",
            "month": "Oct",
            "dates": ["2024-10-27", "2024-10-28", "2024-10-29", "2024-10-30", "2024-10-31", "2024-11-01", "2024-11-02"]
        }).inserted_id
    response = client.post("/enroll", data={
        "exercise": "example_exercise",
        "program_id": str(program_id)
    }, follow_redirects=True)
    enrolled_programs = list(client.application.mongo.db.enrollment.find({"email": "test@example.com"}))
    assert len(enrolled_programs) == 1

def test_cancel_enrollment_successfully(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    with client.application.app_context():
        # Insert mock program and enrollment
        program_id = client.application.mongo.db.program_plan.insert_one({"title": "Yoga Basics"}).inserted_id
        client.application.mongo.db.enrollment.insert_one({"email": "test@example.com", "program": program_id})
    response = client.post("/cancel_enrollment", data={
        "exercise": "yoga",
        "program_id": str(program_id)
    }, follow_redirects=True)
    enrolled_programs = list(client.application.mongo.db.enrollment.find({"email": "test@example.com"}))
    assert len(enrolled_programs) == 0

def test_view_my_programs_with_enrollments(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    with client.application.app_context():
        # Insert mock enrollment and program
        program_id = client.application.mongo.db.program_plan.insert_one({"title": "Cardio Blast", "exercise": "cardio"}).inserted_id
        client.application.mongo.db.enrollment.insert_one({"email": "test@example.com", "program": program_id})
    response = client.get("/my_programs")
    assert b"Cardio Blast" in response.data

def test_redirect_unauthenticated_program_route(client):
    response = client.get("/program?exercise=example_exercise")
    assert response.status_code == 302  # Redirect status
    assert response.location.endswith("/dashboard")  # Redirects to the dashboard
