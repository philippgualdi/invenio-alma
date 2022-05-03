# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Alma Service config class."""


class AlmaServiceConfig:
    """Alma service configuration class."""

    api_host = ""
    api_key = ""
    mms_id_path = "metadata.fields.001"
    ac_id_path = "metadata.fields.009"
    rec_id_path = "id"
    url_path = (
        ".//record//datafield[@ind1='4' and @ind2=' ' "
        "and @tag='856']//subfield[@code='u']"
    )

    controlfields = [
        "001",
        "003",
        "005",
        "006",
        "007",
        "008",
        "009",
    ]

    def build(self, app):
        """Update configuration from flask app."""
        self.api_key = app.config.get("INVENIO_ALMA_API_KEY", "")
        self.api_host = app.config.get("INVENIO_ALMA_API_HOST", "")
        return self

    def _base_url(self):
        """Property get base url for alma rest api."""
        return f"https://{self.api_host}/almaws/v1/bibs"

    def url_get(self, mms_id):
        """Alma rest api get record url.

        :param mms_id (str): alma record id

        :return str: alma api url.
        """
        api_url = (
            self._base_url()
            + f"?mms_id={mms_id}&apikey={self.api_key}&view=full&expand=None"
        )
        return api_url

    def url_put(self, mms_id):
        """Alma rest api put record url.

        :param mms_id (str): alma record id

        :return str: alma api url.
        """
        api_url = self._base_url() + f"/{mms_id}?apikey={self.api_key}"
        return api_url

    def url_post(self):
        """Alma rest api post record url.

        :return str: alma api url.
        """
        api_url = self._base_url() + f"?apikey={self.api_key}"
        return api_url
