Feature: Match SLUG

  SLUGs are matched if each of the alleles of one SLUG are in the other SLUG.

  Scenario Outline: Match SLUGS by allele

    Given the SLUG for patient is <Patient-SLUG>
    And the SLUG for donor is <Donor-SLUG>
    When we perform SLUG match patient and donor
    Then they should be <Matched>

    Examples:
      | Patient-SLUG            | Donor-SLUG              | Matched |
      | HLA-C*07:02+HLA-C*16:01 | HLA-C*07:02+HLA-C*16:01 | Yes     |
      | HLA-A*13:02+HLA-A*13:01 | HLA-A*13:02+HLA-A*30:01 | No      |
      | HLA-A*13:02+HLA-B*13:01 | HLA-A*13:02+HLA-A*30:01 | No      |
