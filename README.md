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

<h3> Setting up Python environment </h3>

There are two ways to set up the Python environment - using [pip](https://pypi.org/project/pip/) or [Conda](https://github.com/conda/conda) to download the required Python packages. 


For Conda, [environment.yml](environment.yml) contains the requirements needed to (hopefully) recreate the environment this was developed in.
  1. Use the terminal or anaconda prompt to run 
       ```
       conda env create -f environment.yml
       ```
     This should automatically create the Conda environment. For further details/help, please refer to the Conda guide on [creating an environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
  2. To activate the envronment, 
       ```
       conda activate extract_pdf
       ```
  3. The `environment.yml` should capture the packages in the pip distribution.

[requirements.txt](requirements.txt)

[download tabula at](https://tabula.technology/)

<h3> Downloading the Code Base </h3>


<h2> How to use? </h2>


<h2> To Do </h2>
Refactor!
