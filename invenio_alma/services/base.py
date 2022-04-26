# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Alma service base module."""

import re
from functools import reduce

from invenio_records_marc21.proxies import current_records_marc21
from lxml import etree


class RecordValueMixin:
    """Alma record value mixin class."""

    @classmethod
    def deep_get(cls, dictionary, keys, default=None):
        """Get value from multiple keys.

        :param dictionary to search
        :param keys str multiple keys
        """
        return reduce(
            lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
            keys.split("."),
            dictionary,
        )

    @classmethod
    def deep_set(cls, dictionary, keys, value):
        """Set value from multiple keys.

        :param dictionary to search
        :param keys str multiple keys
        """
        skeys = keys.split(".")

        pos_list = r"^\[[0-9]+\]$"
        extracted = dictionary
        for key in skeys[:-1]:
            if key in extracted:
                extracted = extracted[key]
            elif re.match(pos_list, key):
                extracted = extracted[int(key[1:-1])]
            else:
                return dictionary
        if keys[-1] in extracted:
            extracted[keys[-1]] = value
        return dictionary


class AlmaBaseService(RecordValueMixin):
    """Alma base record service class."""

    def __init__(self, config):
        """Constructor.

        :param config: A service configuration
        """
        self.config = config


class RepositoryBaseService(AlmaBaseService):
    """Alma repository base service class."""

    def __init__(self, config, record_service=None):
        """Constructor.

        :param config: A service configuration
        :param record_service: A repository service. Default to current_records_marc21
        """
        super().__init__(config)
        self._record_module = (
            record_service if record_service else current_records_marc21
        )

    @property
    def _record_service(self):
        """Marc21 repository records service."""
        return self._record_module.records_service

    def _search(self, identity, **kwargs):
        """Search records in the repository.

        :param identity (str): Itentity used to authenticate in the repository

        :return dict: hits of repository records.
        """
        results = self._record_service.scan(identity, **kwargs)
        results = results.to_dict()
        return results

    @classmethod
    def to_etree(cls, text):
        """Convert string to etree."""
        return etree.fromstring(text.encode("utf-8"))

    def get_records(self, identity, **kwargs):
        """Search records in the repository.

        :param identity (str): Itentity used to authenticate in the repository

        :return []: list of records hit.
        """
        results = self._search(identity, **kwargs)
        records = results.get("hits", {}).get("hits", [])
        return records
