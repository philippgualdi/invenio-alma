# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Alma Service."""

import requests
from lxml import etree
from lxml.builder import E

from .base import BaseService
from .errors import AlmaRESTException


class AlmaRESTService(BaseService):
    """Alma REST service class."""

    @staticmethod
    def get(url):
        """Alma rest api get request.

        :param url (str): url to api

        :raises AlmaRESTException if request was not successful

        :return str: response content
        """
        response = requests.get(url, headers={"accept": "application/xml"})
        if response.status_code >= 400:
            raise AlmaRESTException(code=response.status_code, msg=response.text)
        return response.text

    @staticmethod
    def post(url, data):
        """Alma rest api post request.

        :param url (str): url to api
        :param data (str): payload

        :raises AlmaRESTException if request was not successful

        :return str: response content
        """
        response = requests.post(
            url,
            data,
            headers={"content-type": "application/xml", "accept": "application/xml"},
        )
        if response.status_code >= 400:
            raise AlmaRESTException(code=response.status_code, msg=response.text)
        return response.text

    @staticmethod
    def put(url, data):
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

    @staticmethod
    def _extract_almarecord(data):
        """Extract record from request.

        :param data (str): result list

        :return lxml.Element: extracted record
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        record = etree.fromstring(data)
        # extract single record
        bib = record.xpath(".//bib")
        if len(bib) > 0:
            record = bib[0]
        return record

    def update_url(self, records, new_url):
        """Change url in a record.

        :param records ([Dict]): List of repository records
        :params new_url (str): new repository url. Url must contain '{recid}'
        """
        for record in records:
            mms_id = self.deep_get(record, self.config.mms_id_path)
            rec_id = self.deep_get(record, self.config.rec_id_path)

            # prepare record
            api_url = self.config.url_get(mms_id)
            data = self.get(api_url)
            metadata = self._extract_almarecord(data)

            # extract url subfield
            url_datafield = metadata.xpath(self.config.url_path)

            if len(url_datafield) == 0:
                # No URL subfield in a record
                continue

            url_datafield = url_datafield[0]
            url_datafield.text = new_url.format(recid=rec_id)
            alma_record = etree.tostring(metadata)
            alma_record = alma_record.decode("UTF-8")
            url_put = self.config.url_put(mms_id)
            self.put(url_put, alma_record)

    def create_record(self, metadata):
        """Create a record in Alma.

        :param metadata (Dict): The metadata for the new record.
        """
        # prepare url
        api_url = self.config.url_post()

        # convert metadata to marc21 xml
        record_dict = metadata.get("metadata", {})
        alma_tree = self._convert_metadata(record_dict)
        alma_record = etree.tostring(alma_tree)
        alma_record = alma_record.decode("UTF-8")
        response = self.post(api_url, alma_record)
        return response

    def _convert_metadata(self, obj):
        """Convert the metadata to Marc21 xml."""
        rec = E.record()
        leader = obj.get("leader")
        if leader:
            rec.append(E.leader(leader))

        fields = obj.get("fields", [])

        # items = iteritems(fields)

        for key, value in fields.items():
            # Control fields
            if key in self.config.controlfields:
                controlfield = E.controlfield(value)
                controlfield.attrib["tag"] = key
                rec.append(controlfield)
            else:

                for subfields in value:
                    datafield = E.datafield()
                    datafield.attrib["tag"] = key

                    indicator1 = subfields.get("ind1", " ")
                    indicator2 = subfields.get("ind2", " ")

                    datafield.attrib["ind1"] = indicator1.replace("_", " ")
                    datafield.attrib["ind2"] = indicator2.replace("_", " ")
                    items = subfields.get("subfields", {})
                    for k in items.keys():
                        datafield.append(E.subfield(", ".join(items[k]), code=k))
                rec.append(datafield)
        bib = E.bib()
        bib.append(rec)
        return bib
