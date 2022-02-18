import yaml
from py2neo import Graph

with open("neo4j.yaml", "r") as neo4j_file:
    neo_dict = yaml.safe_load(neo4j_file)
    neo4j_url = neo_dict["neo4j_url"]
    user = neo_dict["user"]
    password = neo_dict["password"]


def cypher_imgt_db_versions():
    query = """
    MATCH (g:GFE)-[e:HAS_WHO]-(w:WHO)
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
    graph = Graph(neo4j_url, user=user, password=password)
    dbs = list_all_db_releases(graph)
    return {"imgt_versions": dbs}, 200


def cypher_gfe_from_who():
    query = """
    MATCH (g:GFE)-[r:HAS_WHO]-(w:WHO)
        WHERE w.name = $who_name
        RETURN g.locus AS locus, g.gfe_name AS gfe, w.name AS who, r.releases AS imgt_versions
    """
    return query


def gfe_from_who(who_name: str):
    graph = Graph(neo4j_url, user=user, password=password)
    cypher = cypher_gfe_from_who()
    response = graph.run(cypher, {"who_name": who_name})
    result = response.next()
    return {
        "locus": result["locus"],
        "gfe": result["gfe"],
        "who": result["who"],
        "imgt_versions": result["imgt_versions"],
    }


def cypher_all_gfe_from_locus():
    query = """
    MATCH (g:GFE)-[:HAS_WHO]-(w:WHO)
    WHERE g.locus = $locus
    RETURN g.gfe_name AS gfe, w.name AS who
    limit 100
    """
    return query


def all_locus_gfe(gene: str):
    graph = Graph(neo4j_url, user=user, password=password)
    cypher = cypher_all_gfe_from_locus()
    response = graph.run(cypher, {"locus": gene})
    allele_gfe_list = []
    for result in response:
        allele_gfe_list.append({"allele": result["who"], "GFE": result["gfe"]})
    return {"gene": gene, "GFEs": allele_gfe_list}
