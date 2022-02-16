from my_project_template.model.slug import SLUG


# SLUG match
# match the SLUG of patient with donor


def slug_match(patient_slug: SLUG, donor_slug: SLUG) -> bool:
    """
    SLUGs are matched if they are equal to each other

    @param patient_slug: Patient SLUG
    @param donor_slug: Donor SLUG
    @return: bool indicating whether they match or not
    """
    return patient_slug == donor_slug
