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
    rec_id = "id"
    url_path = ".//record//datafield[@ind1='4' and @ind2=' ' and @tag='856']//subfield[@code='u']"
    
    @classmethod
    def url_get(cls, mmsid):
        api_url = f"https://{cls.api_host}/almaws/v1/bibs?view=full&expand=None&apikey={cls.api_key}&mms_id={mmsid}"
        return api_url
    
    @classmethod
    def url_put(cls, mmsid):
        api_url = f"https://{cls.api_host}/almaws/v1/bibs/{mmsid}?apikey={cls.api_key}"
        return api_url
