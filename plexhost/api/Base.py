import requests

from ..constant import BASE_URL
from ..errors import InvalidArgument, Forbidden, BadRequest, InternalPanelError


class PlexHostAPI(object):
    """
    Base for the Client

    Attributes
    ----------
    key : str
        The api key necessary to use the client.

    """

    def __init__(self, key: str = None):
        if not key:
            raise InvalidArgument(f"Key was of wrong type: {type(key)}")
        self._key = key
        self._session = requests.Session()
        #self._dummy_test()

    def _get_headers(self):
        """Return the headers for requests internally"""
        return {
            'Authorization': f'Bearer {self._key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def _dummy_test(self):
        """Dummy test to check if the entered key works"""
        req = self._session.get(BASE_URL)
        if req.status_code == 401:
            raise Forbidden("Entered api key is invalid")

    def _parse_response(self, response, detail=False):
        """Parse the response data.
        Optionally includes additional data that specifies the object type
        and requires accessing the data through a nested dictionary.  The
        Client API doesn't include any additional information, but the
        Servers API includes created and updated timestamps in the detailed
        response.
        Args:
             response(dict): A request response object.
             detail(bool): Include additional data from the raw response.
        """
        if detail:
            data = response
        else:
            if response['object'] == 'list':
                data = [item.get('attributes') for item in response.get('data')]
            else:
                data = response.get('attributes')

        return data

    def _request(self, endpoint, method='GET', **kwargs):
        """Make a request to the PlexHost API
        Args:
            endpoint(str): URI for the API
            method(str): Request type, one of ('GET', 'POST', 'DELETE', 'PUT')
            params(dict): Extra parameters to pass to the endpoint,
                    e.g. a query string
            data(dict): POST data
            json(bool): Set to False to return the response object,
                    True for just JSON.  Defaults to returning JSON if possible
                    otherwise the response object.
        Returns:
            response: A HTTP response object or the JSON response depending on
                    the value of the json parameter.
        """
        params = kwargs.pop("params", None)
        data = kwargs.pop("data", None)
        json = kwargs.pop("data", None)

        url = BASE_URL + endpoint if endpoint is not None else ""
        headers = self._get_headers()

        if method == 'GET':
            response = self._session.get(url, params=params, headers=headers)
        elif method == 'POST':
            response = self._session.post(url, params=params, headers=headers,
                                          json=data)
        elif method == 'DELETE':
            response = self._session.delete(url, params=params, headers=headers)
        elif method == 'PUT':
            response = self._session.put(url, params=params, headers=headers,
                                         json=data)
        else:
            raise BadRequest(
                'Invalid request type specified(%s).  Must be one of %r.' % (method, ["GET", "POST", "DELETE", "PUT"]))

        try:
            response_json = response.json()
        except ValueError:
            response_json = {}

        if response.status_code in (400, 422):
            raise InternalPanelError('API Request resulted in errors: %s' %
                                     response_json.get('errors'))
        else:
            response.raise_for_status()

        if json is True:
            return response_json
        elif json is False:

            return response
        else:
            return response_json or response
