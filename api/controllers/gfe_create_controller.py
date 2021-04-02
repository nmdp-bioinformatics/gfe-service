from pygfe.pygfe import pyGFE
from py2neo import Graph
from neo4j.exceptions import ServiceUnavailable
from pygfe.models.error import Error
import logging
import io
import re
import yaml
from pandas import DataFrame
from seqann.sequence_annotation import BioSeqAnn
from pygfe.models.feature import Feature

seqanns = {}
gfe_feats = None
gfe2hla = None
seq2hla = None
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


def gfe_create_post(sequence, imgt_version='3.31.0'):
    """gfe_create_post

    Get all features associated with a locus

    :param locus: Valid HLA locus
    :param sequence: Valid sequence
    :param imgt_version : db version
    :rtype: Typing
    """
    global seqanns
    global gfe_feats
    global gfe2hla
    global seq2hla

    locus = sequence['locus']
    seq = sequence['sequence']

    if '.' in imgt_version:
        db = imgt_version.replace('.', '')
    else:
        db = imgt_version

    if db in seqanns:
        seqann = seqanns[db]
    else:
        seqann = BioSeqAnn(verbose=True, safemode=True,
                           dbversion=db, verbosity=3)
        seqanns.update({db: seqann})
    try:
        graph = Graph(neo4j_url, user=neo4j_user, password=neo4j_password, bolt=False)
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
        typing = pygfe.gfe_create(locus=locus, sequence=seq, imgtdb_version=db)
    except Exception as e:
        print(e)
        log_contents = log_capture_string.getvalue()
        return Error("Type with alignment failed",
                     log=log_contents.split("\n")), 404

    if isinstance(typing, Error):
        log_contents = log_capture_string.getvalue()
        typing.log = log_contents.split("\n")
        return typing, 404

    if not typing:
        log_contents = log_capture_string.getvalue()
        return Error("Type with alignment failed",
                     log=log_contents.split("\n")), 404
    structure_feats = []
    for f in typing['structure']:
        fn = Feature(accession=f.accession, rank=f.rank,
                     term=f.term, sequence=f.sequence)
        structure_feats.append(fn)
    anno_feats = []
    for f in typing['annotation'].structure:
        fn = Feature(accession=f.accession, rank=f.rank,
                     term=f.term, sequence=f.sequence)
        anno_feats.append(fn)
    return {
        'gfe': typing['gfe'],
        'feature': structure_feats,
        'annotation_feature': anno_feats
    }
