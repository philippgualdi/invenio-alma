# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-alma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test Services base."""


from invenio_alma.services.errors import AlmaException, AlmaRESTException


def test_rest_exception():
    error = AlmaRESTException(code=123, msg="TEST")

    assert isinstance(error, AlmaException)
    assert str(error) == "Alma API error code=123 msg='TEST'"
