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
    def _extract_almarecord(cls, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        tree =  etree.fromstring(data)
        test = tree.find(".//bib//record")
        metadata = Marc21Metadata()
        metadata.load(test)
        return metadata

    @classmethod
    def _create_almarecord(cls, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        tree =  etree.fromstring(data)
        root = etree.Element("bib")
        root.append(tree)
        return root
    
    @classmethod
    def get(cls, url):
        data = requests.get(url, headers={"accept": "application/xml"})
        if data.status_code == 200:
            return data.text
        return ""

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
        records = self.get_records(identity, **kwargs)
        
        base_url = self._baseurl()
        base_url = base_url + "&mms_id="
        for record in records:
            mmsid = self.deep_get(record, self.config.mms_id)
            recid = self.deep_get(record, self.config.recid)
            
            api_url = base_url + mmsid
            
            data = self.get(api_url)
            metadata = self._extract_almarecord(data)

            record_url = [new_url.format(recid=recid)]
            record_new = self.deep_set(metadata.json, "metadata.fields.856.[0].subfields.u", record_url)
            metadata_new = Marc21Metadata()
            metadata_new.json = record_new
            record_new = self._create_almarecord(str(record_new))          
