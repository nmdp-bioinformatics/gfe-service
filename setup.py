# coding: utf-8

from setuptools import setup, find_packages

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

with open('requirements.txt') as reqs:
    requirements = reqs.read().split()

setup(
    name="gfe_service",
    version="0.1.1",
    description="GFE REST Service",
    author="CIBMTR",
    author_email='cibmtr-pypi@nmdp.org',
    url="https://github.com/nmdp-bioinformatics/service-act",
    keywords=["Swagger", "GFE REST Service"],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={
        'swagger_server': ['swagger/swagger.yaml']
    },
    install_requires=requirements,
    include_package_data=True,
    long_description="""
    The gfe and annotation services for annotation,notation, types, HLA and db releases. It provides a RESTful API and a 
    simple user interface for converting raw sequence data to GFE results. Sequences can be submitted one at a time. 
    This service uses &lt;a href&#x3D;\&quot;https://github.com/nmdp-bioinformatics/service-feature\&quot;&gt;nmdp-bioinformatics/service-feature&lt;/a&gt; 
    for encoding the raw sequence data and &lt;a href&#x3D;\&quot;https://github.com/nmdp-bioinformatics/HSA\&quot;&gt;nmdp-bioinformatics/HSA&lt;/a&gt; 
    for aligning the raw sequence data. The code is open source, and available on &lt;a href&#x3D;\&quot;https://github.com/nmdp-bioinformatics/gfe-service\&quot;&gt;
    GitHub&lt;/a&gt;.&lt;br&gt;&lt;
    """
)
