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
from lxml.etree import _Element as Element
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
        record =  etree.fromstring(data)
        record = record.xpath(".//bibs")
        return record

    
    @classmethod
    def get(cls, url):
        data = requests.get(url, headers={"accept": "application/xml"})
        if data.status_code == 200:
            return data.text
        return ""

    @classmethod
    def put(cls, url, data):
        return requests.put(url, data, headers={"content-type": "application/xml", "accept": "application/xml"})


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
            
            url_datafield = metadata.xpath(".//bib//record//datafield[@ind1='4' and @ind2=' ' and @tag='856']//subfield[@code='u']")
            if len(url_datafield) == 1:
                url_datafield = url_datafield[0]
            url_datafield.text = new_url.format(recid=recid)
            #record_new = self.deep_set(metadata.json, "metadata.fields.856.[0].subfields.u", record_url)
            alma_record = etree.tostring(metadata)
            alma_record = alma_record.decode("UTF-8")
            api_url = "https://%s/almaws/v1/bibs/%s?apikey=%s" % (
                self.config.api_host,
                mmsid,
                self.config.api_key,
            )
            record_new = self.put(api_url, alma_record)          
