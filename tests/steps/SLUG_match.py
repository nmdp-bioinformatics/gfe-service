from behave import *
from hamcrest import assert_that, is_

from my_project_template.algorithm.match import slug_match
from my_project_template.model.slug import SLUG


@given("the SLUG for patient is {slug}")
def step_impl(context, slug):
    context.patient_slug = SLUG.from_glstring(slug)


@step("the SLUG for donor is {slug}")
def step_impl(context, slug):
    context.donor_slug = SLUG.from_glstring(slug)


@when("we perform SLUG match patient and donor")
def step_impl(context):
    context.matched = slug_match(context.patient_slug, context.donor_slug)


@then("they should be {is_matched}")
def step_impl(context, is_matched):
    matched = is_matched == "Yes"
    assert_that(context.matched, is_(matched))
