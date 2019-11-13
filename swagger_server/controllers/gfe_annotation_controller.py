from pygfe.models.error import Error  # noqa: E501
from pygfe.models.typing import Typing  # noqa: E501
from pygfe.models.feature import Feature

from seqann.sequence_annotation import BioSeqAnn
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import logging
import io
import re

seqanns = {}


def gfeAnnotation_post(sequence, gene, locus=None, imgthla_version="3.31.0"):
    """gfeAnnotation_post

        Get all kir associated with a GFE # noqa: E501

        :param sequence: Valid sequence fasta
        :param gene: the KIR param true or false
        :param locus: Valid Locus
        :rtype: Typing
        """
    global seqanns

    typing = Typing()
    sequence = SeqRecord(seq=Seq(sequence['sequence']))

    if not re.match(".", imgthla_version):
        imgthla_version = ".".join([list(imgthla_version)[0],
                                    "".join(list(imgthla_version)[1:3]),
                                    list(imgthla_version)[3]])

    db = "".join(imgthla_version.split("."))
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

    if db in seqanns:
        seqann = seqanns[db]
    elif gene:
        seqann = BioSeqAnn(verbose=True, safemode=True,
                           dbversion=db, verbosity=3, kir=True)
        seqanns.update({db: seqann})
    else:
        seqann = BioSeqAnn(verbose=True, safemode=True,
                           dbversion=db, verbosity=3)
        seqanns.update({db: seqann})

    try:
        annotation = seqann.annotate(sequence, locus)
    except Exception as e:
        print(e)
        log_contents = log_capture_string.getvalue()
        return Error("An error occured during the annotation",
                     log=log_contents.split("\n")), 404

    if not annotation:
        log_contents = log_capture_string.getvalue()
        return Error("No annotation could be produced",
                     log=log_contents.split("\n")), 404

    if not hasattr(annotation, 'structure'):
        log_contents = log_capture_string.getvalue()
        return Error("No structure was produced",
                     log=log_contents.split("\n")), 404

    feats = []
    for f in annotation.structure:
        fn = Feature(accession=f.accession, rank=f.rank,
                     term=f.term, sequence=f.sequence)
        feats.append(fn)

    typing.features = feats
    typing.gfe = annotation.gfe
    typing.imgtdb_version = imgthla_version
    return typing
