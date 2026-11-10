import httpx
from unittest.mock import patch, Mock

from app.monitor import check_website


def test_website_is_up():

    mock_response = Mock()
    mock_response.status_code = 200

    with patch("app.monitor.httpx.get", return_value=mock_response):

        result = check_website("https://example.com")

    assert result["status"] == "UP"
    assert result["status_code"] == 200
    assert result["error"] is None


 
def test_website_is_down():

    mock_response = Mock()
    mock_response.status_code = 500

    with patch("app.monitor.httpx.get", return_value=mock_response):

        result = check_website("https://example.com")

    assert result["status"] == "DOWN"
    assert result["status_code"] == 500



def test_website_timeout():

    with patch(
        "app.monitor.httpx.get",
        side_effect=httpx.TimeoutException("Request timed out")
    ):

        result = check_website("https://example.com")

    assert result["status"] == "DOWN"
    assert result["error"] == "Request timed out"