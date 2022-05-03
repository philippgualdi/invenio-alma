# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test Services base."""

import json
from unittest import mock

import pytest
from requests.models import Response

from invenio_alma.services.alma import AlmaRESTService
from invenio_alma.services.errors import AlmaRESTException


class TestConfig:
    """Alma service configuration class."""

    api_host = "test.at"
    api_key = "1234567890"
    mms_id_path = "field1"
    ac_id_path = "field9"
    rec_id_path = "id"
    url_path = (
        ".//record//datafield[@ind1='4' and @ind2=' ' "
        "and @tag='856']//subfield[@code='u']"
    )


def mocked_request(*args, **kwargs):
    breakpoint()
    response_content = None
    request_url = kwargs.get("url", None)
    status_code = 500
    if "valid" in request_url:
        response_content = json.dumps("a response")
        status_code = 200
    elif "invalid" in request_url:
        response_content = json.dumps("b response")
        status_code = 401
    response = Response()
    response.status_code = status_code
    response._content = str.encode(response_content)
    return response


def test_base_service():
    config = TestConfig()
    service = AlmaRESTService(config)
    assert isinstance(service.config, type(config))


@mock.patch("requests.get", side_effect=mocked_request)
def test_alma_service_get(request):

    config = TestConfig()

    service = AlmaRESTService(config)
    response = service.get("https://test.at/valid_url")


@mock.patch("requests.get", side_effect=mocked_request)
def test_alma_service_get_exception(mock_get):
    breakpoint()
    config = TestConfig()

    service = AlmaRESTService(config)
    with pytest.raises(AlmaRESTException):
        response = service.get("https://test.at/invalid_url")
