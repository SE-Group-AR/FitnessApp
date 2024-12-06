# Test for BMI calculation with very small inputs
def test_bmi_calculation_very_small_inputs(client):
    response = client.post('/bmi_calc', data={
        'weight': '0.5',
        'height': '0.5'
    })
    bmi = calc_bmi(0.5, 0.5)
    bmi_category = get_bmi_category(bmi)

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert str(bmi) in soup.text
    assert bmi_category in soup.text

# Test for BMI calculation with very large inputs
def test_bmi_calculation_very_large_inputs(client):
    response = client.post('/bmi_calc', data={
        'weight': '500',
        'height': '2.5'
    })
    bmi = calc_bmi(500, 2.5)
    bmi_category = get_bmi_category(bmi)

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert str(bmi) in soup.text
    assert bmi_category in soup.text

# Test for handling negative weight
def test_negative_weight_input(client):
    response = client.post('/bmi_calc', data={
        'weight': '-70',
        'height': '1.75'
    })
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'Invalid Category' in soup.text

# Test for handling negative height
def test_negative_height_input(client):
    response = client.post('/bmi_calc', data={
        'weight': '70',
        'height': '-1.75'
    })
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'Invalid Category' in soup.text

# Test for handling non-numeric inputs for both fields
def test_non_numeric_inputs(client):
    response = client.post('/bmi_calc', data={
        'weight': 'abc',
        'height': 'xyz'
    })

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'Invalid Category' in soup.text

# Test for handling zero weight
def test_zero_weight_input(client):
    response = client.post('/bmi_calc', data={
        'weight': '0',
        'height': '1.75'
    })

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'Invalid Category' in soup.text

# Test for handling zero height
def test_zero_height_input(client):
    response = client.post('/bmi_calc', data={
        'weight': '70',
        'height': '0'
    })

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'Invalid Category' in soup.text

# Test for form validation without submitting any data
def test_form_submission_without_data(client):
    response = client.post('/bmi_calc', data={})

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'Invalid Category' in soup.text

# Test for BMI calculation with edge-case height and weight
def test_edge_case_inputs(client):
    response = client.post('/bmi_calc', data={
        'weight': '45.5',
        'height': '1.50'
    })
    bmi = calc_bmi(45.5, 1.50)
    bmi_category = get_bmi_category(bmi)

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert str(bmi) in soup.text
    assert bmi_category in soup.text

# Test for handling whitespace in inputs
def test_whitespace_in_inputs(client):
    response = client.post('/bmi_calc', data={
        'weight': ' 70 ',
        'height': ' 1.75 '
    })
    bmi = calc_bmi(70, 1.75)
    bmi_category = get_bmi_category(bmi)

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    assert str(bmi) in soup.text
    assert bmi_category in soup.text
