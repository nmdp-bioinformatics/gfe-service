from flask import request
import pandas
import yaml
from neo4j.exceptions import ServiceUnavailable
from py2neo import Graph

from my_project_template.model.allele import InvalidAllele
from my_project_template.my_project_template import match

with open("neo4j.yaml", "r") as neo4j_file:
    neo_dict = yaml.safe_load(neo4j_file)


def cypher_imgt_db_versions():
    query = """
    MATCH(g:GFE)-[e:HAS_WHO]-(w:WHO)
	    WITH COLLECT(DISTINCT e.releases) AS releases
	    UNWIND REDUCE(output=[], r IN releases| output + r) as dbs
	    RETURN COLLECT(DISTINCT dbs) as HLA_DB_VERSIONS
        ORDER BY HLA_DB_VERSIONS DESC
    """
    return query


def list_all_db_releases(graph):
    cypher = cypher_imgt_db_versions()
    response = graph.run(cypher)
    db_versions = response.next()
    return db_versions["HLA_DB_VERSIONS"]


def imgt_versions():
    neo4j_url = neo_dict["neo4j_url"]
    user = neo_dict["user"]
    password = neo_dict["password"]
    graph = Graph(neo4j_url, user=user, password=password)
    dbs = list_all_db_releases(graph)
    return {"imgt_versions": dbs}, 200


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
