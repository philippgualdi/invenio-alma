# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-Alma is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from .base import AlmaBaseServiceConfig

class AlmaServiceConfig(AlmaBaseServiceConfig):
    """Alma service configuration class."""

    mms_id = "metadata.fields.001"
    ac_id = "metadata.fields.009"
