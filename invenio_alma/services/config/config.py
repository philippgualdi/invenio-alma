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
    mms_id = "metadata.fields.001"
    ac_id = "metadata.fields.009"
    rec_id = "id"
    url_path = (
        ".//record//datafield[@ind1='4' and @ind2=' ' "
        "and @tag='856']//subfield[@code='u']"
    )

    @classmethod
    def build(cls, app):
        """Update configuration from flask app."""
        setattr(cls, "api_key", app.config.get("INVENIO_ALMA_API_KEY", ""))
        setattr(cls, "api_host", app.config.get("INVENIO_ALMA_API_HOST", ""))
        return cls

    @classmethod
    def url_get(cls, mmsid):
        """Alma rest api get record url.

        :return str: alma api url.
        """
        api_url = (
            f"https://{cls.api_host}/almaws/v1/bibs?mms_id={mmsid}&"
            f"expand=None&apikey={cls.api_key}&view=full"
        )
        return api_url

    @classmethod
    def url_put(cls, mmsid):
        """Alma rest api put record url.

        :return str: alma api url.
        """
        api_url = f"https://{cls.api_host}/almaws/v1/bibs/{mmsid}?apikey={cls.api_key}"
        return api_url
