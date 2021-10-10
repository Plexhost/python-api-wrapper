from .api.Base import PlexHostAPI


class PlexHostClient(PlexHostAPI):
    """
    Represents a client connected to the dashboard.

    Attributes
    ----------
    key : str
        The api key necessary to use the client.

    """

    def get_servers(self):
        """List[:class:`Server`]: The servers which the user has access to"""
        print(self._request(""))
