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


class Allele:
    """
    A Class I allele is an allele of Locus 'HLA-A', 'HLA-B', 'HLA-C'
    """

    def __init__(self, locus: str, allele: str):
        """
        Validate the Class I locus and allele first.

        @param locus: Class I Locus
        @param allele: Class I Allele
        """
        self.validate(locus, allele)
        self.allele = allele
        self.locus = locus

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Allele):
            return self.locus == other.locus and self.allele == other.allele
        return False

    def __lt__(self, other):
        if isinstance(other, Allele):
            return self.allele < other.allele
        return False

    def __str__(self) -> str:
        if self.allele.startswith("HLA-"):
            return self.allele
        return f"{self.locus}*{self.locus}"

    @staticmethod
    def validate(locus: str, allele: str):
        if locus not in ["HLA-A", "HLA-B", "HLA-C"]:
            raise InvalidAllele(f"{locus} is Not a valid locus")
        if "*" not in allele and ":" not in allele:
            raise InvalidAllele("f{allele} is Not a valid allele")

    @classmethod
    def from_fullname(cls, allele):
        if not allele.startswith("HLA-"):
            raise InvalidAllele(f"{allele} is not a fully-named allele")
        locus = allele.split("*")[0]
        return Allele(locus, allele)


class InvalidAllele(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
