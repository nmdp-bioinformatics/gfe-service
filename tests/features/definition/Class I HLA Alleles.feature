Feature: SLUGs of Class I HLA Alleles

  Class I HLA Alleles are alleles on genomic loci HLA-A, HLA-B and HLA-C.
  SLUGs are Single Locus Un-phased Genotypes made up of a pair of alleles.
  The alleles are lexicographically sorted.

  Scenario Outline: HLA Class I Locus SLUG

  Each gene of HLA-A, HLA-B and HLA-C have a pair of alleles, one from each parent.

    Given The Locus of Gene is <Locus>
    And The first allele is <Allele1>
    And The second allele is <Allele2>
    When I create an un-phased genotype
    Then I get the single locus un-phased genotype <SLUG>

    Examples: Valid Class I Alleles
      | Locus | Allele1     | Allele2     | SLUG                    |
      | HLA-A | HLA-A*13:02 | HLA-A*30:01 | HLA-A*13:02+HLA-A*30:01 |
      | HLA-B | HLA-B*38:01 | HLA-B*07:02 | HLA-B*07:02+HLA-B*38:01 |
      | HLA-C | HLA-C*07:02 | HLA-C*16:01 | HLA-C*07:02+HLA-C*16:01 |
