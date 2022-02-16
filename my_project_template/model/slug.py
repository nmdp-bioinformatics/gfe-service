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

from .allele import Allele


class SLUG:
    """
    SLUGs are Single Locus Un-phased Genotypes made up of a pair of alleles.
    The alleles are lexicographically sorted.
    """

    def __init__(self, allele_1: Allele, allele_2: Allele) -> None:
        """
        SLUGs are single locus genotypes with alleles in sorted order

        @param allele_1:
        @param allele_2:
        """
        if allele_1 < allele_2:
            self.allele_1 = allele_1
            self.allele_2 = allele_2
        else:
            self.allele_1 = allele_2
            self.allele_2 = allele_1

    def __str__(self) -> str:
        """
        String version of SLUG is in GL String format

        @return: gl-string format of SLUG
        """
        return f"{self.allele_1}+{self.allele_2}"

    def __eq__(self, other: object) -> bool:
        """
        2 SLUGs are equal if the individual alleles are equal
        to each other.

        @param other:
        @return: True indicating whether 2 SLUGS are equal
        """
        if isinstance(other, SLUG):
            return self.allele_1 == other.allele_1 and self.allele_2 == other.allele_2
        return False

    @classmethod
    def from_glstring(cls, slug):
        allele_1, allele_2 = slug.split("+")
        slug = SLUG(Allele.from_fullname(allele_1), Allele.from_fullname(allele_2))
        return slug
