class Subuser:
    def __init__(self, props):
        self._props = props

    def get_uuid(self):
        return self._props["uuid"]

    def get_username(self):
        return self._props["username"]

    def get_email(self):
        return self._props["email"]

    def get_image(self):
        return self._props["image"]

    def has_2fa_enabled(self):
        """bool: If the user has 2fa enabled."""
        return self._props["2fa_enabled"]

    def get_created(self):
        return self._props["created_at"]

    def permissions(self):
        """List[str]: List over the subusers permissions"""
        return self._props["permissions"]