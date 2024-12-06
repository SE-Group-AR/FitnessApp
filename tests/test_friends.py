import pytest
from bs4 import BeautifulSoup

# Test for rendering the friends page when user is logged in with friends


def test_render_friends_page(client):
    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.user.insert_one({'name': 'John Doe', 'email': 'friend1@example.com'})
    client.application.mongo.db.friends.insert_one({'sender': 'test@example.com', 'receiver': 'friend1@example.com', 'accept': True})

    response = client.get('/friends')

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'My Friends' in soup.text
    assert 'friend1@example.com' in soup.text


# Test for pending friend requests
def test_pending_requests(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.friends.insert_one({'sender': 'friend2@example.com', 'receiver': 'test@example.com', 'accept': False})

    response = client.get('/friends')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'Sent Requests' in soup.text
    assert 'friend2@example.com' in soup.text


# Test for rendering the friends page when the user is not logged in
def test_friends_page_not_logged_in(client):
    response = client.get('/friends')
    assert response.status_code == 302

# Test for rendering the friends page with no friends
def test_render_friends_page_no_friends(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.get('/friends')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'My Friends' in soup.text
    assert 'No friends yet' in soup.text


# Test for pending requests sent by the user
def test_sent_pending_requests(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.friends.insert_one({'sender': 'test@example.com', 'receiver': 'friend3@example.com', 'accept': False})

    response = client.get('/friends')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'Pending Friend Requests' in soup.text
    assert 'friend3@example.com' in soup.text


# Test for declining a friend request
def test_decline_friend_request(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.friends.insert_one({'sender': 'friend4@example.com', 'receiver': 'test@example.com', 'accept': False})

    response = client.post('/friends/decline', data={'sender': 'friend4@example.com'})
    assert response.status_code == 200

    friend_request = client.application.mongo.db.friends.find_one({'sender': 'friend4@example.com', 'receiver': 'test@example.com'})
    assert friend_request is None


# Test for accepting a friend request
def test_accept_friend_request(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.friends.insert_one({'sender': 'friend5@example.com', 'receiver': 'test@example.com', 'accept': False})

    response = client.post('/friends/accept', data={'sender': 'friend5@example.com'})
    assert response.status_code == 200

    friend_request = client.application.mongo.db.friends.find_one({'sender': 'friend5@example.com', 'receiver': 'test@example.com'})
    assert friend_request['accept'] is True


# Test for searching friends
def test_search_friends(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.user.insert_one({'name': 'Jane Smith', 'email': 'friend6@example.com'})

    response = client.get('/friends/search?query=Jane')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'friend6@example.com' in soup.text


# Test for removing a friend
def test_remove_friend(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.friends.insert_one({'sender': 'test@example.com', 'receiver': 'friend7@example.com', 'accept': True})

    response = client.post('/friends/remove', data={'email': 'friend7@example.com'})
    assert response.status_code == 200

    friend_record = client.application.mongo.db.friends.find_one({'sender': 'test@example.com', 'receiver': 'friend7@example.com'})
    assert friend_record is None


# Test for rendering friends page with a mix of accepted and pending requests
def test_friends_page_with_mixed_requests(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.friends.insert_one({'sender': 'test@example.com', 'receiver': 'friend8@example.com', 'accept': True})
    client.application.mongo.db.friends.insert_one({'sender': 'friend9@example.com', 'receiver': 'test@example.com', 'accept': False})

    response = client.get('/friends')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'friend8@example.com' in soup.text
    assert 'friend9@example.com' in soup.text


# Test for preventing duplicate friend requests
def test_prevent_duplicate_friend_request(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    client.application.mongo.db.friends.insert_one({'sender': 'test@example.com', 'receiver': 'friend10@example.com', 'accept': False})

    response = client.post('/friends/request', data={'receiver': 'friend10@example.com'})
    assert response.status_code == 400

    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'Request already sent' in soup.text


# Test for handling a non-existent friend in requests
def test_non_existent_friend_request(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/friends/accept', data={'sender': 'nonexistent@example.com'})
    assert response.status_code == 404

    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'Friend request not found' in soup.text
