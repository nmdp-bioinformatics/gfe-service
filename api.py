import yaml
from py2neo import Graph

from gfe_service import query

with open("config/config.yaml", "r") as neo4j_file:
    neo_dict = yaml.safe_load(neo4j_file)
    neo4j_url = neo_dict["neo4j_url"]
    user = neo_dict["user"]
    password = neo_dict["password"]
    if not user:
        raise ValueError("No Neo4j User supplied")
    if not password:
        raise ValueError("No Neo4j Password supplied")
    if not neo4j_url:
        raise ValueError("No Neo4j URL supplied")

graph = Graph(neo4j_url, user=user, password=password)


def imgt_versions():
    cypher = query.imgt_db_versions()
    response = graph.run(cypher)
    db_versions = response.next()
    dbs = db_versions["HLA_DB_VERSIONS"]
    return {"imgt_versions": dbs}, 200


def gfe_from_ipd(ipd_name: str):
    cypher = query.gfe_from_ipd()
    response = graph.run(cypher, {"ipd_name": ipd_name})
    result = response.next()
    return {
        "locus": result["locus"],
        "gfe": result["gfe"],
        "allele": result["allele"],
        "imgt_versions": result["imgt_versions"],
    }, 200


def all_locus_gfe(gene: str, version: str = None):
    cypher = query.all_gfe_from_locus(version)
    response = graph.run(cypher, {"locus": gene, "version": version})
    allele_gfe_list = []
    for result in response:
        allele_gfe_list.append(
            {
                "allele": result["allele"],
                "GFE": result["gfe"],
                "releases": result["releases"],
            }
        )
    return {"gene": gene, "GFEs": allele_gfe_list}


def gfe_sequence(gfe: str):
    cypher = query.sequence_from_gfe()
    response = graph.run(cypher, {"gfe": gfe})
    result = response.next()
    return {"sequence": result["sequence"], "GFE": gfe}


def features_from_allele(ipd_name: str):
    cypher = query.features_from_allele()
    response = graph.run(cypher, {"ipd_name": ipd_name})
    features = response.data()

    gfes = set([feature["gfe"] for feature in features])
    if len(gfes) != 1:
        raise Exception("Only one GFE is expected!")
    gfe = gfes.pop()
    features = [
        {k: v for k, v in feature.items() if k != "gfe"} for feature in features
    ]

    # TODO: Build in ranks of features into database
    # so genetic ordering is built in already (5' utr - (exon - intron)s - 3' UTR)
    features_ordered = (
        [feature for feature in features if feature["term"] == "FIVE_PRIME_UTR"]
        + (
            [
                feature
                for rank in range(1, 9)
                for feature in (
                    [
                        feature
                        for feature in features
                        if feature["term"] == "EXON" and feature["rank"] == str(rank)
                    ]
                    + [
                        feature
                        for feature in features
                        if feature["term"] == "INTRON" and feature["rank"] == str(rank)
                    ]
                )
            ]
        )
        + [feature for feature in features if feature["term"] == "THREE_PRIME_UTR"]
    )

    return {"gfe": gfe, "features": features_ordered}
