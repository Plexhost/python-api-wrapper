import requests

from plexhost.errors import BadRequest


class Server():
    def __init__(self, client, props, details=None):
        self._props = props
        self._details = details
        self._client = client

    def is_owner(self):
        """bool: If the key is the owner of the server"""
        return self._props["server_owner"]

    def get_id(self):
        """str: The id used by our systems to describe your server"""
        return self._props["identifier"]

    def get_internalId(self):
        """str: The internal id used by our systems to describe your server"""
        return self._props["internal_id"]

    def get_name(self):
        """str: The name of the server"""
        return self._props["name"]

    def get_description(self):
        """str: The description of the server"""
        return self._props["description"]

    def get_node(self):
        """str: The node which the server is located on"""
        return self._props["node"]

    def get_SFTP(self):
        """Dict[str]: The ip and port details to connect to the server's sftp"""
        return self._props["sftp_details"]

    def get_status(self):
        """str: The status of the server"""
        return self._props["status"]

    def is_suspended(self):
        """bool: If the server is suspended"""
        return self._props["is_suspended"]

    def is_installing(self):
        """bool: If the server is installing"""
        return self._props["is_installing"]

    def is_transferring(self):
        """bool: If the server is installing"""
        return self._props["is_transferring"]

    def get_usage(self):
        """Returns the server usage in a dict

        state: str - running/offline
        resources: Dict[int]
            - memory_bytes
            - cpu_absolute
            - disk_bytes
            - network_rx_bytes
            - network_tx_bytes

        """
        response = self._client._parse_response(
            self._client._request('servers/%s/resources' % self.get_id()))
        self._props["is_suspended"] = response["is_suspended"]
        return {"state": response["current_state"], "resources": response["resources"]}

    def send_command(self, command: str):
        """Sends a console command to the server

        Arguments:
            command(str): Command to send
        """
        self._client._request(endpoint='servers/%s/command' % self.get_id(), method='POST', data={'command': command},
                              json=False)

    def start(self):
        """Start the server"""
        self._power_action("start")

    def restart(self):
        """Restart the server"""
        self._power_action("restart")

    def stop(self):
        """Stop the server"""
        self._power_action("stop")

    def kill(self):
        """Kill the server"""
        self._power_action("kill")

    def get_users(self):
        return self.get_subusers()

    def get_subusers(self):
        """List[Dict]: Lists dicts over the servers subusers"""
        response = self._client._parse_response(self._client._request(endpoint='servers/%s/users' % self.get_id()))
        return response

    def _power_action(self, action: str = "start"):
        """Sends a action to the server (power)

        Args:
            action(str): The action to send to the server. (start, restart, stop, kill)
        """

        if action.lower() not in ["start", "restart", "stop", "kill"]:
            raise BadRequest(
                'Invalid action specified(%s).  Must be one of %r.' % (action, ["start", "restart", "stop", "kill"]))

        self._client._request(endpoint='servers/%s/power' % self.get_id(), method='POST', data={'signal': action},
                              json=False)

    def list_files(self, path: str = None):
        """List files on the server

        Args:
            path(str): Path to list files in (e.g 'plugins')
        """

        params = {'directory': path} if path is not None else {}
        response = self._client._parse_response(
            self._client._request(endpoint='servers/%s/files/list' % self.get_id(), params=params))
        return response
