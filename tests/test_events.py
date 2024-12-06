import pytest
from unittest.mock import MagicMock
from fitnessapp.application import getFriends
from bs4 import BeautifulSoup

def test_events_user_not_logged_in(client):
    response = client.get("/events")
    assert b"User not logged in" in response.data

def test_events_no_friends(client, mocker):
    mocker.patch("fitnessapp.application.getFriends", return_value=[])
    response = client.get("/events", follow_redirects=True)
    assert b'invited_friend' not in response.data  # No choices rendered

def test_events_invalid_date_format(client, mocker, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    mocker.patch("fitnessapp.application.getFriends", return_value=["friend@example.com"])
    
    response = client.post("/events", data={
        "exercise": "Yoga",
        "date": "2024/10/30",  # Invalid format
        "start_time": "09:00",
        "end_time": "10:00",
        "invited_friend": "friend@example.com"
    })
    events = list(app.mongo.db.events.find({"host": "test@example.com"}))
    assert len(events) == 0

def test_events_missing_required_fields(client, mocker, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    mocker.patch("fitnessapp.application.getFriends", return_value=["friend@example.com"])
    
    response = client.post("/events", data={
        "date": "2024-10-30",
        "start_time": "09:00",
        "end_time": "10:00",
        "invited_friend": "friend@example.com"
    })
    events = list(app.mongo.db.events.find({"host": "test@example.com"}))
    assert len(events) == 0

def test_events_invalid_friend_invite(client, mocker, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    mocker.patch("fitnessapp.application.getFriends", return_value=["friend@example.com"])
    response = client.post("/events", data={
        "exercise": "Yoga",
        "date": "2024-10-30",
        "start_time": "09:00",
        "end_time": "10:00",
        "invited_friend": "invalid_friend@example.com"
    })
    events = list(app.mongo.db.events.find({"host": "test@example.com"}))
    assert len(events) == 0

def test_events_view_existing_events(client, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    app.mongo.db.events.insert_one({
        "exercise": "Yoga",
        "host": "test@example.com",
        "date": "2024-10-30",
        "start_time": "09:00",
        "end_time": "10:00",
        "invited_friend": "friend@example.com"
    })
    
    response = client.get("/events")
    assert b"Yoga" in response.data

def test_events_add_event(client, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    app.mongo.db.events.delete_many({"host": "test@example.com"})
    app.mongo.db.friends.insert_one({'sender': 'test@example.com', 'receiver': 'friend@example.com', 'accept': True})

    response = client.post("/events", data={
        "exercise": "Yoga",
        "date": "2024-10-30",
        "start_time": "09:00",
        "end_time": "10:00",
        "invited_friend": "friend@example.com"
    })

    assert b"Yoga" in response.data
    assert b"2024-10-30" in response.data
    
    events = list(app.mongo.db.events.find({"host": "test@example.com"}))
    assert len(events) == 1

def test_events_display_friends_in_dropdown(client, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    app.mongo.db.friends.insert_many([
        {"sender": "test@example.com", "receiver": "friend1@example.com", "accept": True},
        {"sender": "test@example.com", "receiver": "friend2@example.com", "accept": True}
    ])
    
    response = client.get("/events")
    assert b"friend1@example.com" in response.data
    assert b"friend2@example.com" in response.data

def test_events_correct_time_format(client):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    response = client.get("/events")
    soup = BeautifulSoup(response.data, 'html.parser')
    inputs = soup.find_all("input", class_="form-control")
    time_inputs = [input_elem for input_elem in inputs if input_elem.get("type") == "time"]
    assert len(time_inputs) == 2

def test_get_friends(client):
    with client.application.app_context():
        client.application.mongo.db.friends.insert_many([
            {"sender": "test@example.com", "receiver": "friend1@example.com", "accept": True},
            {"sender": "test@example.com", "receiver": "friend2@example.com", "accept": False}
        ])
        friends = getFriends("test@example.com")
        assert friends == ["friend1@example.com"]

def test_events_redirect_non_logged_in(client):
    response = client.get("/events", follow_redirects=True)
    assert b"Login to access events" in response.data

def test_events_overlap(client, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    app.mongo.db.events.insert_one({
        "exercise": "Yoga",
        "host": "test@example.com",
        "date": "2024-10-30",
        "start_time": "09:00",
        "end_time": "10:00"
    })
    
    response = client.post("/events", data={
        "exercise": "Pilates",
        "date": "2024-10-30",
        "start_time": "09:30",
        "end_time": "10:30"
    })
    
    assert b"Time slot overlaps with an existing event" in response.data

def test_events_past_date(client, app):
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
    
    response = client.post("/events", data={
        "exercise": "Yoga",
        "date": "2020-01-01",
        "start_time": "09:00",
        "end_time": "10:00",
        "invited_friend": "friend@example.com"
    })
    
    assert b"Cannot create an event in the past" in response.data
