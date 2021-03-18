import io
import logging
import yaml
from neo4j.exceptions import ServiceUnavailable
from py2neo import Graph
from pygfe.models.error import Error

with open("swagger_server/neo4j.yaml", "r") as neo4j_file:
    neo_dict = yaml.safe_load(neo4j_file)


def get_hla_gfe_by(graph, locus, imgt_version):
    cypher = "MATCH (n:IMGT_HLA)-[r:HAS_GFE]-(g:GFE) WHERE n.locus = \"" + locus + \
             "\" AND r.imgt_release = \"" + imgt_version + \
             "\" RETURN n.name as hla, g.name as gfe"
    result = graph.run(cypher).data()
    return result


def releases_locus_get(imgt_release_version, locus, neo4j_url=neo_dict['neo4j_url'], user=neo_dict['user'],
                       password=neo_dict['password']):
    """releases_locus_get

        Get Alleles and their corresponding GFE By Locus and IMGT version

    :param imgt_release_version: Valid imgt release version number
    :param locus: Valid locus name
    :rtype: list of Alleles and their corresponding GFE
    """

    log_capture_string = io.StringIO()
    logger = logging.getLogger('')
    logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler(log_capture_string)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)-35s - %(levelname)-5s '
        '- %(funcName)s %(lineno)d: - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    try:
        graph = Graph(neo4j_url,
                      user=user,
                      password=password,
                      bolt=False)
    except ServiceUnavailable as err:
        log_contents = log_capture_string.getvalue()
        log_data = log_contents.split("\n")
        log_data.append(str(err))
        return Error("Failed to connect to graph", log=log_data), 404

    imgt_version = "".join(imgt_release_version.split("."))

    try:
        hla_list = get_hla_gfe_by(graph, locus, imgt_version)
    except Exception as e:
        log_contents = log_capture_string.getvalue()
        print("The Error", e)
        return Error("hla list failed", log=log_contents.split("\n")), 404

    if isinstance(hla_list, Error):
        log_contents = log_capture_string.getvalue()
        hla_list.log = log_contents.split("\n")
        return hla_list, 404

    if not hla_list:
        log_contents = log_capture_string.getvalue()
        return Error("no data record found", log=log_contents.split("\n")), 404

    return hla_list
