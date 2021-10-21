import pytest
from server import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


# ERROR 1 --> OK
def test_show_summary_displays_error_message_with_bad_email(client):
    email = "test@test.co"
    response = client.post('/showSummary',
                           data={"email": email},
                           follow_redirects=True)
    expected_flash_message = b"Sorry, that email was not found."
    assert response.status_code == 200
    assert expected_flash_message in response.data

