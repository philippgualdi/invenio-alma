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
        self._record_module= record_service if record_service else current_records_marc21
    
    @property
    def _record_service(self):
        return self._record_module.records_service
    
    
    def search(self, identity, **kwargs):
        result_list = self._record_service.scan(identity, **kwargs)
        l = list(result_list._results)
        self.deep_get(l[0].to_dict(),self.config.mms_id)
        return result_list
    