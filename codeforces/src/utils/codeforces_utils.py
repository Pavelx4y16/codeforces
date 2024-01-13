from requests import Response, JSONDecodeError

from codeforces.src.utils.utils import validate_arguments


@validate_arguments
class ParsedResponse:
    def __validate_init_arguments(self, response):
        assert isinstance(response, Response)

    def __init__(self, response: Response):
        self.response = response
        self._parse(response)

    def _json(self, response):
        try:
            return response.json()
        except JSONDecodeError:
            return None

    def _parse(self, response):
        self.url = response.url
        self.status_code = response.status_code
        self.is_redirected = any(_response.is_redirect for _response in response.history)
        self.text = response.text

        json = self._json(response)
        if self.status_code == 200:
            self.result = json['result'] if json else response.text
        else:
            self.reason = json['comment']
