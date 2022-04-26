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
        record = record.xpath(".//bib")[0] # extract single record
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

        for record in records:
            mmsid = self.deep_get(record, self.config.mms_id)
            recid = self.deep_get(record, self.config.rec_id)
            
            # prepare record
            api_url = self.config.url_get(mmsid)
            data = self.get(api_url)
            metadata = self._extract_almarecord(data)
            
            #extract url subfield
            url_datafield = metadata.xpath(self.config.url_path)
            
            if len(url_datafield) == 0:
                # No URL in record
                continue
            
            url_datafield = url_datafield[0]
            url_datafield.text = new_url.format(recid=recid)
            alma_record = etree.tostring(metadata)
            alma_record = alma_record.decode("UTF-8")
            url_put = self.config.url_put(mmsid)
            record_new = self.put(url_put, alma_record)
