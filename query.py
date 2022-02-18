def imgt_db_versions():
    query = """
    MATCH (g:GFE)-[e:HAS_WHO]-(w:WHO)
        WITH COLLECT(DISTINCT e.releases) AS releases
        UNWIND REDUCE(output=[], r IN releases| output + r) as dbs
        RETURN COLLECT(DISTINCT dbs) as HLA_DB_VERSIONS
        ORDER BY HLA_DB_VERSIONS DESC
    """
    return query


def gfe_from_who():
    query = """
    MATCH (g:GFE)-[r:HAS_WHO]-(w:WHO)
        WHERE w.name = $who_name
        RETURN g.locus AS locus, g.gfe_name AS gfe, w.name AS who, r.releases AS imgt_versions
    """
    return query


def all_gfe_from_locus():
    query = """
    MATCH (g:GFE)-[:HAS_WHO]-(w:WHO)
    WHERE g.locus = $locus
    RETURN g.gfe_name AS gfe, w.name AS who
    limit 100
    """
    return query


def sequence_from_gfe():
    query = """
    MATCH (g:GFE)-[:HAS_SEQUENCE]-(s:Sequence)
    WHERE g.gfe_name = $gfe return s.sequence as sequence;
    """
    return query
