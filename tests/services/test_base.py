# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test Services base."""


from invenio_alma.services.base import BaseService


class TestConfig:
    """Alma service configuration class."""

    api_host = ""
    api_key = ""
    mms_id_path = "metadata.fields.001"
    ac_id_path = "metadata.fields.009"
    rec_id_path = "id"
    url_path = (
        ".//record//datafield[@ind1='4' and @ind2=' ' "
        "and @tag='856']//subfield[@code='u']"
    )


def test_base_service():
    config = TestConfig()
    base = BaseService(config)
    assert isinstance(base.config, type(config))


def test_base_service_deep_get():

    config = TestConfig()
    base = BaseService(config)

    # default value
    obj = {"test": "value"}
    test = base.deep_get(obj, "invenio")
    assert test == None

    obj = {"test": "value"}
    test = base.deep_get(obj, "invenio", default="invenio")
    assert test == "invenio"

    # one key
    obj = {"test": "value"}
    test = base.deep_get(obj, "test")
    assert test == "value"

    obj = {
        "test": {"field": "TheValue", "field1": {"Invenio": "value123"}},
        "metadata": {"leader": "1234567890"},
    }
    test = base.deep_get(obj, "test.field1")
    assert test == {"Invenio": "value123"}
