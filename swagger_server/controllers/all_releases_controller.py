import io
import logging
import yaml
from neo4j.exceptions import ServiceUnavailable
from py2neo import Graph
from pygfe.models.error import Error

with open("swagger_server/neo4j.yaml", "r") as neo4j_file:
    neo_dict = yaml.safe_load(neo4j_file)


def all_db_imgt():
    query = " MATCH(n: IMGT_HLA)-[e: HAS_FEATURE]-(feat:FEATURE)" \
            + "RETURN DISTINCT e.imgt_release AS HLA_DB ORDER BY e.imgt_release DESC"
    return query


def list_all_db_releases(graph):
    cypher = all_db_imgt()
    response_data = graph.run(cypher).to_data_frame()
    return list(response_data.HLA_DB)


def allreleases_get(neo4j_url=neo_dict['neo4j_url'], user=neo_dict['user'],
                    password=neo_dict['password']):
    """allreleases_get

        Get all db releases

    :rtype: list of available db
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

    try:
        db_releases = list_all_db_releases(graph)
    except Exception as e:
        log_contents = log_capture_string.getvalue()
        print("The Error", e)
        return Error("Server Error getting IMGT versions.", log=log_contents.split("\n")), 404

    if isinstance(db_releases, Error):
        log_contents = log_capture_string.getvalue()
        db_releases.log = log_contents.split("\n")
        return db_releases, 404

    if not db_releases:
        log_contents = log_capture_string.getvalue()
        return Error("no data record found", log=log_contents.split("\n")), 404
    return db_releases
