import yaml
from py2neo import Graph

import query

with open("neo4j.yaml", "r") as neo4j_file:
    neo_dict = yaml.safe_load(neo4j_file)
    neo4j_url = neo_dict["neo4j_url"]
    user = neo_dict["user"]
    password = neo_dict["password"]

graph = Graph(neo4j_url, user=user, password=password)


def imgt_versions():
    cypher = query.imgt_db_versions()
    response = graph.run(cypher)
    db_versions = response.next()
    dbs = db_versions["HLA_DB_VERSIONS"]
    return {"imgt_versions": dbs}, 200


def gfe_from_who(who_name: str):
    cypher = query.gfe_from_who()
    response = graph.run(cypher, {"who_name": who_name})
    result = response.next()
    return {
        "locus": result["locus"],
        "gfe": result["gfe"],
        "who": result["who"],
        "imgt_versions": result["imgt_versions"],
    }, 200


def all_locus_gfe(gene: str):
    cypher = query.all_gfe_from_locus()
    response = graph.run(cypher, {"locus": gene})
    allele_gfe_list = []
    for result in response:
        allele_gfe_list.append({"allele": result["who"], "GFE": result["gfe"]})
    return {"gene": gene, "GFEs": allele_gfe_list}


def gfe_sequence(gfe: str):
    cypher = query.sequence_from_gfe()
    response = graph.run(cypher, {"gfe": gfe})
    result = response.next()
    return {"sequence": result["sequence"], "GFE": gfe}
