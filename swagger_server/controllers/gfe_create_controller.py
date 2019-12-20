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
neo_file = open("swagger_server/neo4j.yaml", "r")
neo_dict = yaml.safe_load(neo_file)


def gfecreate_post(locus, sequence, imgt_version, neo4j_url=neo_dict['neo4j_url'], user=neo_dict['user'],
                   password=neo_dict['password']):  # noqa: E501
    """gfecreate_post

    Get all features associated with a locus

    :param locus: Valid HLA locus
    :param sequence: Valid sequence
    :param imgt_version : db version
    :rtype: Typing
    """
    imgthla_version = imgt_version
    global seqanns
    global gfe_feats
    global gfe2hla
    global seq2hla
    sequence = sequence['sequence']
    log_capture_string = io.StringIO()
    logger = logging.getLogger('')
    logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler(log_capture_string)
    formatter = logging.Formatter('%(asctime)s - %(name)-35s - %(levelname)-5s'
                                  ' - %(funcName)s %(lineno)d: - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    if not re.match(".", imgthla_version):
        imgthla_version = ".".join([list(imgthla_version)[0],
                                    "".join(list(imgthla_version)[1:3]),
                                    list(imgthla_version)[3]])

    db = "".join(imgthla_version.split("."))
    if db in seqanns:
        seqann = seqanns[db]
    else:
        seqann = BioSeqAnn(verbose=True, safemode=True,
                           dbversion=db, verbosity=3)
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
        typing = pygfe.gfe_create(locus=locus, sequence=sequence,
                                  imgtdb_version=db)
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
    structute_feats = []
    for f in typing['structure']:
        fn = Feature(accession=f.accession, rank=f.rank,
                     term=f.term, sequence=f.sequence)
        structute_feats.append(fn)
    anno_feats = []
    for f in typing['annotation'].structure:
        fn = Feature(accession=f.accession, rank=f.rank,
                     term=f.term, sequence=f.sequence)
        anno_feats.append(fn)
    return {
        'gfe': typing['gfe'],
        'feature': structute_feats,
        'annotation_feature': anno_feats
    }
