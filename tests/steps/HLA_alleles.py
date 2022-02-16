from behave import *
from hamcrest import assert_that, is_

from my_project_template.model.allele import Allele
from my_project_template.model.slug import SLUG


@given("The Locus of Gene is {locus}")
def step_impl(context, locus):
    context.locus = locus


@step("The first allele is {allele1}")
def step_impl(context, allele1):
    context.allele_1 = Allele(context.locus, allele1)


@step("The second allele is {allele2}")
def step_impl(context, allele2):
    context.allele_2 = Allele(context.locus, allele2)


@when("I create an un-phased genotype")
def step_impl(context):
    context.slug = SLUG(context.allele_1, context.allele_2)


@then("I get the single locus un-phased genotype {slug}")
def step_impl(context, slug):
    assert_that(str(context.slug), is_(slug))
