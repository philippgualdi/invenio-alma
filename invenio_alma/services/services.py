# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-Alma is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Alma Service."""

import requests

from .base import RepositoryBaseService
from lxml import etree
from invenio_records_marc21.services.record.metadata import Marc21Metadata

class AlmaRESTService(RepositoryBaseService):
    def _baseurl(self):
        api_url = "https://%s/almaws/v1/bibs?view=full&expand=None&apikey=%s" % (
            self.config.api_host,
            self.config.api_key,
        )
        return api_url

    @classmethod
    def get(cls, url):
        return requests.get(url, headers={"accept": "application/xml"})

    @classmethod
    def put(cls, url, data):
        return requests.put(url, data, headers={"accept": "application/xml"})


class AlmaService(AlmaRESTService):
    """Alma service class."""

    def __init__(self, config, record_service=None):
        """Constructor.

        :param config: A service configuration
        """
        super().__init__(config, record_service)

    def update_url(self, identity, new_url, **kwargs):
        mmsids = self.get_mmsids(identity, **kwargs)
        base_url = self._baseurl()
        base_url = base_url + "&mms_id="
        for mmsid in mmsids:
            api_url = base_url + mmsid
            data = self.get(api_url)
            tree =  etree.fromstring(data.text.encode("utf-8"))
            test = tree.find(".//bib//record")
            metadata = Marc21Metadata()
            metadata.load(test)
            subfields = self.deep_get(metadata.json, "metadata.fields.856")
            tes = subfields[0].get("subfields", {}).get("u")
            etree.tostring(test)
        return mmsids
