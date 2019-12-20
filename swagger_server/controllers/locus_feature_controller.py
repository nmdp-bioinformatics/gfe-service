from seqann.gfe import GFE
from pygfe.models.error import Error
import logging
import io


def locusfeature_get(locus):  # noqa: E501
    """locusfeature_get

    Get all features associated with a locus # noqa: E501

    :param locus: Valid HLA locus
    :rtype: list of features
    """
    gfe = GFE()

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
        feats = gfe.locus_features(locus)
    except Exception as e:
        print(e)
        log_contents = log_capture_string.getvalue()
        return Error("failed to load the feature of given locus",
                     log=log_contents.split("\n")), 404

    if isinstance(feats, Error):
        log_contents = log_capture_string.getvalue()
        feats.log = log_contents.split("\n")
        return feats, 404

    if not feats:
        log_contents = log_capture_string.getvalue()
        return Error("no feature associated with the given locus",
                     log=log_contents.split("\n")), 404

    return feats
