# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test Services base."""

import pytest
from flask import Flask

from invenio_alma.services.config import AlmaServiceConfig


class PytestAlmaServiceConfig(AlmaServiceConfig):
    def __init__(self):
        pass


def test_config_service():

    config = PytestAlmaServiceConfig()


    assert hasattr(config, "api_host")
    assert config.api_host == ""

    assert hasattr(config, "api_key")
    assert config.api_key == ""

    assert hasattr(config, "mms_id_path")
    assert config.mms_id_path == "metadata.fields.001"

    assert hasattr(config, "ac_id_path")
    assert config.ac_id_path == "metadata.fields.009"

    assert hasattr(config, "rec_id_path")
    assert config.rec_id_path == "id"

    assert hasattr(config, "url_path")
    assert (
        config.url_path == ".//record//datafield[@ind1='4' and @ind2=' ' "
        "and @tag='856']//subfield[@code='u']"
    )


def test_config_service_build_default():
    app = Flask("testapp")
    config = AlmaServiceConfig()

    config.build(app)

    assert hasattr(config, "api_host")
    assert config.api_host == ""

    assert hasattr(config, "api_key")
    assert config.api_key == ""

    assert hasattr(config, "mms_id_path")
    assert config.mms_id_path == "metadata.fields.001"

    assert hasattr(config, "ac_id_path")
    assert config.ac_id_path == "metadata.fields.009"

    assert hasattr(config, "rec_id_path")
    assert config.rec_id_path == "id"

    assert hasattr(config, "url_path")
    assert (
        config.url_path == ".//record//datafield[@ind1='4' and @ind2=' ' "
        "and @tag='856']//subfield[@code='u']"
    )


def test_config_service_build():
    app = Flask("testapp")
    app.config.update(
        {"INVENIO_ALMA_API_KEY": "test", "INVENIO_ALMA_API_HOST": "test.at"}
    )
    config = AlmaServiceConfig()

    config.build(app)

    assert hasattr(config, "api_host")
    assert config.api_host == "test.at"

    assert hasattr(config, "api_key")
    assert config.api_key == "test"
