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

from .base import AlmaBaseService
from invenio_records_marc21.proxies import current_records_marc21


class AlmaService(AlmaBaseService):
    """Alma service class."""

    def __init__(self, config, record_service=None):
        """Constructor.

        :param config: A service configuration
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

    def update_url(self, identity, **kwargs):
        return
