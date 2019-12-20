from pygfe.pygfe import pyGFE
from py2neo import Graph
from neo4j.exceptions import ServiceUnavailable
from pygfe.models.error import Error
import logging
import io
import yaml
from pandas import DataFrame
from seqann.sequence_annotation import BioSeqAnn

seqanns = {}
gfe_feats = None
gfe2hla = None
seq2hla = None
neo_file = open("swagger_server/neo4j.yaml", "r")
neo_dict = yaml.safe_load(neo_file)


def releases_locus_get(imgt_releases, locus, neo4j_url=neo_dict['neo4j_url'], user=neo_dict['user'],
                       password=neo_dict['password']):
    """releases_locus_get

        Get all db releases

    :param imgt_releases: Valid imgt releases verion
    :param locus: Valid imgt releases verion
    :rtype: list of available db
    """
    global seqanns
    global gfe_feats
    global gfe2hla
    global seq2hla
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

    db = "".join(imgt_releases.split("."))
    if db in seqanns:
        seqann = seqanns[db]
    else:
        seqann = BioSeqAnn(verbose=True,
                           safemode=True, dbversion=db, verbosity=3)
        seqanns.update({db: seqann})

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

    if (not isinstance(gfe_feats, DataFrame)
            or not isinstance(seq2hla, DataFrame)):
        pygfe = pyGFE(graph=graph, seqann=seqann,
                      load_gfe2hla=True, load_seq2hla=True,
                      load_gfe2feat=True, verbose=True)
        gfe_feats = pygfe.gfe_feats
        seq2hla = pygfe.seq2hla
        gfe2hla = pygfe.gfe2hla
    else:
        pygfe = pyGFE(graph=graph, seqann=seqann,
                      gfe2hla=gfe2hla,
                      gfe_feats=gfe_feats,
                      seq2hla=seq2hla,
                      verbose=True)
    try:
        hla_list = pygfe.list_db_by_locus_imgt(locus, imgt_releases)
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
