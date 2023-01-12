import time

import pytest
import requests

from codeforces.src.utils.codeforces_utils import ParsedResponse


def test_parsed_request_good():
    time.sleep(2)
    good_response = requests.get(f"https://codeforces.com/api/user.info", params={'handles': "Pavelx4y16"})
    parsed_response = ParsedResponse(good_response)

    assert parsed_response.status_code == 200
    assert isinstance(parsed_response.result, list) and len(parsed_response.result) == 1


def test_parsed_request_bad():
    time.sleep(2)
    bad_response = requests.get(f"https://codeforces.com/api/user.info", params={'handles': "Pavelx4"})
    parsed_response = ParsedResponse(bad_response)

    assert parsed_response.status_code == 400
    with pytest.raises(AttributeError):
        parsed_response.result
    assert "handles" in parsed_response.reason


def test_parsed_request_redirect():
    time.sleep(2)
    redirected_response = requests.get(f"https://codeforces.com/profile/tim2005")
    parsed_response = ParsedResponse(redirected_response)

    assert parsed_response.status_code == 200
    assert "Weldfy" in parsed_response.url
