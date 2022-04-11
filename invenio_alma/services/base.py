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

class RecordValueMixin:
    """Alma record value mixin class."""

    def deep_get(dictionary, keys, default=None):
        """get value from multiple keys
        .param dictionary to search
        :param keys str multiple keys
        """
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)
    
class AlmaBaseService(RecordValueMixin):
    """Alma record service class."""
    
    def __init__(self, config):
        """Constructor.

        :param config: A service configuration
        """
        self.config = config