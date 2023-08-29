import io
import logging

import yaml
from neo4j.exceptions import ServiceUnavailable
from pandas import Series
from py2neo import Graph
from pygfe.models import Feature
from pygfe.models.error import Error
from pygfe.pygfe import lc

with open("neo4j.yaml", "r") as neo_config:
    neo4j_dict = yaml.safe_load(neo_config)
    neo4j_url = neo4j_dict['neo4j_url']
    neo4j_user = neo4j_dict['user']
    neo4j_password = neo4j_dict['password']

logger = logging.getLogger('')
logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

log_capture_string = io.StringIO()
# create console handler and set level to INFO
ch = logging.StreamHandler(log_capture_string)
formatter = logging.Formatter(
    '%(asctime)s - %(name)-35s - %(levelname)-5s '
    '- %(funcName)s %(lineno)d: - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

get_features_cypher_query = """
MATCH(gfe:GFE)-[f1:HAS_FEATURE]-(f:FEATURE)
WHERE gfe.name = "{gfe}"
RETURN 
     f.locus AS locus,
     f.name AS term,
     f.rank AS rank,
     f1.accession AS accession,
     f.sequence AS sequence
""".strip()

get_imgt_hla_cypher_query = """
MATCH(gfe:GFE)<-[:HAS_GFE]-(hla:IMGT_HLA)
WHERE gfe.name = "{gfe}"
RETURN hla.name AS imgt_name
""".strip()


def create_feature(feature_row: Series) -> Feature:
    feature = Feature(accession=feature_row['accession'],
                      rank=feature_row['rank'],
                      sequence=feature_row['sequence'],
                      term=lc(feature_row['term']))
    return feature


def find_features_get(gfe: str):
    """Get all features associated with a GFE

    :param gfe: Valid gfe of locus
    :type gfe: str
    """
    try:
        graph = Graph(neo4j_url, user=neo4j_user, password=neo4j_password, bolt=False)
    except ServiceUnavailable as err:
        log_contents = log_capture_string.getvalue()
        log_data = log_contents.split("\n")
        log_data.append(str(err))
        return Error("Failed to connect to graph", log=log_data), 404

    if graph:
        seq_features = graph.run(get_features_cypher_query.format(gfe=gfe)).to_data_frame()
        features = seq_features.apply(create_feature, axis=1)
        hla = graph.run(get_imgt_hla_cypher_query.format(gfe=gfe)).next()
        return {
            'gfe': gfe,
            'features': features.to_list(),
            'imgt_name': hla.get('imgt_name')
        }

    log_contents = log_capture_string.getvalue()
    log_data = log_contents.split("\n")
    return Error("Error getting data", log=log_data), 404
