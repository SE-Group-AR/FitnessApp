def test_register_missing_fields(client):
    response = client.post('/register', data={
        'username': '',
        'email': '',
        'password': '',
        'confirm_password': ''
    })
    assert response.status_code == 400
    assert b'All fields are required' in response.data


def test_login_missing_fields(client):
    response = client.post('/login', data={
        'email': '',
        'password': ''
    })
    assert response.status_code == 400
    assert b'All fields are required' in response.data


def test_google_login_callback_invalid_code(client, mocker):
    mocker.patch('requests.post', side_effect=lambda *args, **kwargs: MagicMock(status_code=400))
    response = client.get('/login/callback?code=invalid-code')
    assert response.status_code == 400
    assert b'Invalid authorization code' in response.data


def test_profile_update_success(client, app):
    with client:
        app.mongo.db.user.insert_one({
            'email': 'test@example.com',
            'name': 'Test User',
            'pwd': generate_password_hash('password')
        })
        with client.session_transaction() as sess:
            sess['email'] = 'test@example.com'

        response = client.post('/update-profile', data={
            'weight': 65,
            'height': 170,
            'goal': 75,
            'target_weight': 68
        })
        assert response.status_code == 200
        profile = app.mongo.db.profile.find_one({'email': 'test@example.com'})
        assert profile['weight'] == '65'
        assert profile['height'] == '170'
        assert profile['goal'] == '75'
        assert profile['target_weight'] == '68'


def test_profile_update_failure_no_session(client):
    response = client.post('/update-profile', data={
        'weight': 65,
        'height': 170,
        'goal': 75,
        'target_weight': 68
    })
    assert response.status_code == 403
    assert b'User not logged in' in response.data


def test_password_reset_request_success(client, app):
    app.mongo.db.user.insert_one({
        'email': 'test@example.com',
        'name': 'Test User',
        'pwd': generate_password_hash('password')
    })
    response = client.post('/password-reset', data={
        'email': 'test@example.com'
    })
    assert response.status_code == 200
    assert b'Reset link sent' in response.data


def test_password_reset_request_invalid_email(client, app):
    response = client.post('/password-reset', data={
        'email': 'nonexistent@example.com'
    })
    assert response.status_code == 400
    assert b'Email not found' in response.data


def test_password_reset_success(client, app):
    token = 'valid-reset-token'
    app.mongo.db.user.insert_one({
        'email': 'test@example.com',
        'name': 'Test User',
        'pwd': generate_password_hash('password'),
        'reset_token': token
    })
    response = client.post(f'/password-reset/{token}', data={
        'password': 'newpassword',
        'confirm_password': 'newpassword'
    })
    assert response.status_code == 200
    user = app.mongo.db.user.find_one({'email': 'test@example.com'})
    assert user['pwd'] != generate_password_hash('password')  # Password should be updated


def test_password_reset_failure_mismatched_passwords(client):
    token = 'valid-reset-token'
    response = client.post(f'/password-reset/{token}', data={
        'password': 'newpassword1',
        'confirm_password': 'newpassword2'
    })
    assert response.status_code == 400
    assert b'Passwords do not match' in response.data


def test_password_reset_invalid_token(client):
    response = client.post('/password-reset/invalid-token', data={
        'password': 'newpassword',
        'confirm_password': 'newpassword'
    })
    assert response.status_code == 400
    assert b'Invalid or expired reset token' in response.data
