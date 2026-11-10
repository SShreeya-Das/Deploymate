import time
import httpx


def check_website(url: str) -> dict:

    start_time = time.perf_counter()

    try:
        response = httpx.get(
            url,
            timeout=10,
            follow_redirects=True
        )

        end_time = time.perf_counter()

        response_time = round(
            (end_time - start_time) * 1000, 2
        )

        status_code = response.status_code

        is_online = 200 <= status_code < 400

        return {
            "url": url,
            "status": "UP" if is_online else "DOWN",
            "status_code": status_code,
            "response_time_ms": response_time,
            "error": None
        }

    except httpx.TimeoutException:

        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": None,
            "error": "Request timed out"
        }

    except httpx.RequestError as error:

        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": None,
            "error": str(error)
        }