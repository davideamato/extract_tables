<h1> Extract Tables from PDF </h1>
According to internal specifications, this script:

1. Extracts key information from tables in a pdf
2. Structures information for an excel workbook
3. Produces an excel workbook as output

This does not always result in the "correct" result due to the inconsistency and variety of the input pdfs.
Therefore, this has been written to account for the fact that it will fail at points. The aim is to capture the
most commonly occuring cases to reduce the overall workload.

<h2> Core Dependency </h2>

This utilises the python package [tabula](https://tabula-py.readthedocs.io/en/latest/tabula.html) to read tables within
a pdf. As this package is a python wrapper of [tabula-java](https://github.com/tabulapdf/tabula-java), has [java as a dependency](https://pypi.org/project/tabula-py/).

Why Tabula and not [Camelot](https://camelot-py.readthedocs.io/en/master/index.html)? The pdfs to be analysed resulted in Camelot throwing an error while Tabula did not. 

<h2> Installation </h2>


There are two ways to set up the Python environment - using [

[download tabula at](https://tabula.technology/)

<h2> How to use? </h2>


<h2> To Do </h2>
Refactor!
