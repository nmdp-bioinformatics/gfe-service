# -*- coding: utf-8 -*-

#
#    gfe_service GFE Service.
#    Copyright (c) 2021 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#


"""Tests for `gfe_service` package."""

import pytest


@pytest.fixture
def supported_genes():
    """Sample pytest fixture.

    See more at: https://doc.pytest.org/en/latest/fixture.html
    """
    return ["HLA-A", "HLA-B", "HLA-C"]


def test_content(supported_genes):
    """Sample pytest test function with the pytest fixture as an argument."""
    assert "HLA-A" in supported_genes
