# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Alma Service."""

import requests
from lxml import etree

from .base import RepositoryBaseService
from .errors import AlmaRESTException


class AlmaRESTService(RepositoryBaseService):
    """Alma REST service class."""

    @classmethod
    def _extract_almarecord(cls, data):
        """Extract record from request.

        :param data (str): result list

        :return str: extracted record
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        record = etree.fromstring(data)
        # extract single record
        record = record.xpath(".//bib")[0]
        return record

    @classmethod
    def get(cls, url):
        """Alma rest api get request.

        :param url (str): url to api

        :raises AlmaRESTException if request was not successful

        :return str: response content
        """
        response = requests.get(url, headers={"accept": "application/xml"})
        if response.status_code >= 400:
            raise AlmaRESTException(code=response.status_code, msg=response.text)
        return response.text

    @classmethod
    def put(cls, url, data):
        """Alma rest api put request.

        :param url (str): url to api
        :param data (str): payload

        :raises AlmaRESTException if request was not successful

        :return str: response content
        """
        response = requests.put(
            url,
            data,
            headers={"content-type": "application/xml", "accept": "application/xml"},
        )
        if response.status_code >= 400:
            raise AlmaRESTException(code=response.status_code, msg=response.text)
        return response.text


class AlmaService(AlmaRESTService):
    """Alma service class."""

    def update_url(self, identity, new_url, **kwargs):
        """Change url in a record.

        :param identity (str): Itentity used to authenticate in the repository
        """
        records = self.get_records(identity, **kwargs)

        for record in records:
            mmsid = self.deep_get(record, self.config.mms_id)
            recid = self.deep_get(record, self.config.rec_id)

            # prepare record
            api_url = self.config.url_get(mmsid)
            data = self.get(api_url)
            metadata = self._extract_almarecord(data)

            # extract url subfield
            url_datafield = metadata.xpath(self.config.url_path)

            if len(url_datafield) == 0:
                # No URL subfield in a record
                continue

            url_datafield = url_datafield[0]
            url_datafield.text = new_url.format(recid=recid)
            alma_record = etree.tostring(metadata)
            alma_record = alma_record.decode("UTF-8")
            url_put = self.config.url_put(mmsid)
            self.put(url_put, alma_record)
