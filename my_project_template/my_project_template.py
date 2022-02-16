# -*- coding: utf-8 -*-

#
#    my_project_template My Project Template.
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
from .algorithm.match import slug_match
from .model.slug import SLUG


def match(patient_slug_glstring, donor_slug_glstring):
    """
    Perform match on GL String versions of SLUGs

    @param patient_slug_glstring: Patient's SLUG in GL String format
    @param donor_slug_glstring: Donor's SLUG in GL String format
    @return: bool indicating Match or No Match
    """
    patient_slug = SLUG.from_glstring(patient_slug_glstring)
    donor_slug = SLUG.from_glstring(donor_slug_glstring)
    matched = slug_match(patient_slug, donor_slug)
    return donor_slug, matched, patient_slug
