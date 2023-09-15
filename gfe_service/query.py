def imgt_db_versions():
    query = """
    MATCH (g:GFE)-[e:HAS_IPD_ALLELE]-(a:IPD_Allele)
        WITH COLLECT(DISTINCT e.releases) AS releases
        UNWIND REDUCE(output=[], r IN releases| output + r) as dbs
        RETURN COLLECT(DISTINCT dbs) as HLA_DB_VERSIONS
        ORDER BY HLA_DB_VERSIONS DESC
    """
    return query


def gfe_from_ipd():
    query = """
    MATCH (g:GFE)-[r:HAS_IPD_ALLELE]-(a:IPD_Allele)
        WHERE a.name = $ipd_name
        RETURN g.locus AS locus, g.name AS gfe, a.name AS allele, r.releases AS imgt_versions
    """
    return query


def all_gfe_from_locus(version: str):
    if version:
        query = """
      MATCH (g:GFE)-[r:HAS_IPD_ALLELE]-(a:IPD_Allele)
      WHERE g.locus = $locus AND $version IN r.releases
      RETURN g.name AS gfe, a.name AS allele, r.releases AS releases
      """
    else:
        query = """
      MATCH (g:GFE)-[r:HAS_IPD_ALLELE]-(a:IPD_Allele)
      WHERE g.locus = $locus
      RETURN g.name AS gfe, a.name AS allele, r.releases AS releases
      """
    return query


def sequence_from_gfe():
    query = """
    MATCH (g:GFE)-[:HAS_SEQUENCE]-(s:Sequence)
    WHERE g.name = $gfe return s.sequence as sequence
    """
    return query


def features_from_allele():
    query = """
    MATCH (a:IPD_Allele)-[:HAS_IPD_ALLELE]-(g:GFE)-[:HAS_FEATURE]-(f:Feature)
    WHERE (a.name = $ipd_name)
    RETURN DISTINCT
        g.name as gfe,
        f.term as term,
        f.accession as accession,
        f.rank as rank,
        f.sequence as sequence
    """
    return query
