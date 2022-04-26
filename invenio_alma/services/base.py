# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-Alma is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from functools import reduce
from lxml import etree
from invenio_records_marc21.proxies import current_records_marc21


class RecordValueMixin:
    """Alma record value mixin class."""

    @classmethod
    def deep_get(cls, dictionary, keys, default=None):
        """get value from multiple keys

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
        """set value from multiple keys

        :param dictionary to search
        :param keys str multiple keys
        """
        skeys = keys.split(".")
        import re
        pos_list = r"^\[[0-9]+\]$"
        d = dictionary
        for key in skeys[:-1]:
            if key in d:
                d = d[key]
            elif re.match(pos_list,key):
                d = d[int(key[1:-1])]
            else:
                return dictionary
        if keys[-1] in d:
            d[keys[-1]] = value
        return dictionary


class AlmaBaseService(RecordValueMixin):
    """Alma record service class."""

    def __init__(self, config):
        """Constructor.

        :param config: A service configuration
        """
        self.config = config


class RepositoryBaseService(AlmaBaseService):
    """Alma record service class."""

    def __init__(self, config, record_service=None):
        """Constructor.

        :param config: A service configuration
        :param record_service: A repository service. Default current_records_marc21
        """
        super().__init__(config)
        self._record_module = (
            record_service if record_service else current_records_marc21
        )

    @property
    def _record_service(self):
        return self._record_module.records_service

    def _search(self, identity, **kwargs):
        results = self._record_service.scan(identity, **kwargs)
        result_list = list(results._results)
        return result_list

    @classmethod
    def to_etree(cls, text):
        return etree.fromstring(text.encode("utf-8"))
        
    def get_mmsids(self, identity, **kwargs):
        """_summary_

        Args:
            identity (str): _description_

        Returns:
            []: list of mms_id
        """
        result_list = self._search(identity, **kwargs)
        mmsids = []
        for result in result_list:
            value = self.deep_get(result.to_dict(), self.config.mms_id)
            if value:
                mmsids.append(value)
        return mmsids

    def get_records(self, identity, **kwargs):
        """Search records

        Args:
            identity (str): _description_

        Returns:
            []: list of records 
        """
        result_list = self._search(identity, **kwargs)
        records = []
        for result in result_list:
            records.append(result.to_dict())
        return records