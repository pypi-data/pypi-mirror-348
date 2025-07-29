# PhotogrammetryTools
This is a repository gathering tools for preparing and processing images for photogrammetry.

Version: 0.0.0

# Installation

## Environment

Use the `pypho.yml` to create an environment with most dependencies installed.

	conda env create -f pypho.yml

Then activate the environment with `conda activate pypho`

Additionnal dependencies might be needed for special usages:
- `pyembree` for multiple ray casting: `pip install pyembree`

## Notebook test

### Local Notebooks
The folder `notebooks/` provides Jupyter notebooks to showcase the avaliable tools\
and allow you to test the proposed tools.

To make your own tests while making sure the notebooks work you can duplicate the proposed notebooks in the same folder.

To avoid versionning the test notebooks, please have their name match: *-local.ipynb

### Remove local information from the versionning

`.gitattributes` is setting up a `jq` filter `nbstrip` to remove metadata and execution counts from notebooks before commit.

To be effective, you must add the following piece of script in the .git/config:

	[filter "nbstrip"]
	clean = "jq --indent 1 \
			'(.cells[] | select(has(\"execution_count\")) | .execution_count) = null  \
			| .metadata = {\"language_info\": {\"name\": \"python\", \"pygments_lexer\": \"ipython3\"}} \
			| .cells[].metadata = {} \
			'"
