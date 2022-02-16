from flask import request

from my_project_template.model.allele import InvalidAllele
from my_project_template.my_project_template import match


def slug_match_controller():
    if request.json:
        # Check the request
        try:
            patient_slug_glstring = request.json["patient_slug"]
            donor_slug_glstring = request.json["donor_slug"]
        except KeyError:
            return {"message": "Invalid data in patient_slug/donor_slug"}, 400
        # Perform match
        try:
            donor_slug, matched, patient_slug = match(
                patient_slug_glstring, donor_slug_glstring
            )
            matched_result = "Match" if matched else "No Match"
            return {
                "matched": matched_result,
                "patient_slug": str(patient_slug),
                "donor_slug": str(donor_slug),
            }, 200
        except InvalidAllele as e:
            return {"message": e.message}, 400

    # if no data is sent
    return {"message": "No input provided"}, 404
