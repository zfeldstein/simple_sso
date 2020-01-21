
def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    # assert b"Welcome to the Flask User Management Example!" in response.data
    # assert b"Need an account?" in response.data
    # assert b"Existing user?" in response.data
