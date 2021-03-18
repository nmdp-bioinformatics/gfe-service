from seqann.sequence_annotation import BioSeqAnn
from seqann.gfe import GFE
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from pygfe.models.error import Error  # noqa: E501
from pygfe.models.feature import Feature
import io
import logging


def gfeNotation_post(sequence, locus, gene):
    """
    gfeNotation_post
        GFE notations associated with the sequence

        :param locus: Valid HLA locus
        :param sequence: Valid sequence
        :param gene : Kir true or false
        :rtype: Feature and gfe
    """
    kir = gene
    sequence = SeqRecord(seq=Seq(sequence['sequence']))
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

    gfe = GFE()
    if kir:
        seqann = BioSeqAnn(kir=True)
    else:
        seqann = BioSeqAnn()

    try:
        annotation = seqann.annotate(sequence)
    except Exception as e:
        print(e)
        log_contents = log_capture_string.getvalue()
        return Error("An error occured during the annotation",
                     log=log_contents.split("\n")), 404
    try:
        res_feature, res_gfe = gfe.get_gfe(annotation, locus)
    except Exception as e:
        print(e)
        log_contents = log_capture_string.getvalue()
        return Error("An error occured in getting the gfe of annotation",
                     log=log_contents.split("\n")), 404
    feats = []
    for f in res_feature:
        fn = Feature(accession=f.accession, rank=f.rank,
                     term=f.term, sequence=f.sequence)
        feats.append(fn)
    return {
        'gfe': res_gfe,
        'feature': feats
    }
