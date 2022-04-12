


class AlmaBaseServiceConfig:
    """Alma service base configuration class."""

    @classmethod
    def build(cls, app):
        """."""
        setattr(cls, 'api_key', app.config.get("INVENIO_ALMA_API_KEY"))
        setattr(cls, 'api_host', app.config.get("INVENIO_ALMA_API_HOST"))
        return cls
