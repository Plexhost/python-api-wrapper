from .api import Base
from .api.Server import Server


class PlexHostClient(Base.PlexHostAPI):
    """
    Represents a client connected to the dashboard.

    Attributes
    ----------
    key : str
        The api key necessary to use the client.

    """

    def get_servers(self):
        """List[:class:`Server`]: The servers which the user has access to"""
        servers = []
        response = self._parse_response(self._request(''))
        for server in response:
            servers.append(Server(props=server, client=self))
        return servers

    def get_server(self, identifier: str):
        """:class:`Server`: The server with the id 'identifier'"""
        response = self._parse_response(self._request('servers/%s' % identifier))
        return Server(props=response, client=self)
