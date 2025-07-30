# Python Package for Converting IPython Jupyter Notebooks to Jekyll Readable (.md, .html)

This repository contains tools for converting .ipynb files to markdown and/or html so that they can be used by Jekyll (the static compiler that GitHub pages uses)

## Notebook Conversion Workflow

This tool converts Jupyter Notebooks (`.ipynb`) into HTML pages suitable for use in a static Jekyll site, with front matter, navigation, and asset handling.

1. **Input**  
   - Jupyter Notebooks (`.ipynb`) located in a configured `nb_read_path` directory.
   - Configuration dictionary specifying read/write paths and asset subdirectories.

2. **Processing**
   - Parses metadata: title, topics (from first cell) using keyword globs "Topics" 
   - Converts notebook to HTML using `nbconvert`.
   - Fixes relative links for images and assets (e.g., `src="/images/foo.png"` → Jekyll-compatible paths).
   - Adds YAML front matter for Jekyll layout integration.
   - Inserts Prev/Next navigation links between notebooks.

3. **Output**
   - Writes processed notebooks as `.html` files to `nb_write_path`.
   - Copies any linked notebook assets (e.g., images) to the correct `assets/` subfolder for Jekyll to use.

## Installation

Install from PyPI using pip: 
```bash
pip3 install nbconvertjkl
```

or clone the repository and install using:
```bash
# clone repo and activate virtualenv then install requirements
pip install -r requirements.txt
```

## Usage

The first cell of your notebooks are used to write front matter and topics to the table of contents of the Jekyll site. The first cell should contain the title and topics of the notebook. The tool will automatically parse this information and add it to the generated HTML files.

The title and topics in the first cell should look like this:
```markdown
# My Notebook Title

 **Topics Covered**
 - Topic 1
 - Topic 2
```

Everything else like (permalink, layout, the wrapping --- … ---) is auto-generated.  Likewise, footer/nav HTML is injected based on the converter’s config flags (no special notebook keywords needed).

To build the site from your notebooks use:
```bash
python -m nbconvertjkl
# OR if you want to build/run automatically in a gh action or something
python -m nbconvertjkl --yes
```


## Contributing

To contribute or work locally:

1. **Set up the environment**
   ```bash
   # Clone the repo
   git clone https://github.com/yourusername/nbconvertjkl.git
   cd nbconvertjkl

   # Make sure you are using a compatible Python version
   python3 --version # if not, use pyenv to install the correct version
   pyenv install 3.6.15
   pyenv shell 3.6.15

   # (Optional) Create a virtualenv
   python3 -m venv .venv
   source .venv/bin/activate

   # Install dependencies and package in editable mode
   pip install -e .
   ```
2. Run the tool locally
   ```bash
   # Main entry point
   python -m nbconvertjkl --config path/to/config.yml
   ```

3. **Run tests**
   ```bash
   # Run tests
   pytest tests/
   ```

4. **(Optional) Build and check package locally**
   Building is  handles in the release-build job of the github action on release. 
   
   But if you want to build locally for debugging or whatever, you can do so:
   ```bash
   # Build and check package
   python -m build # will gnerate source + wheel (dist/nbconvertjkl-0.1.0-py3-none-any.whl and dist/nbconvertjkl-0.1.0.tar.gz)
   python -m twine check dist/* # check the package metadata is valid before uploading to PyPI
   ```

   You can also test install from local build:
   ```bash
   pip uninstall nbconvertjkl # remove any previous version
   pip install dist/nbconvertjkl-0.1.0-py3-none-any.whl # install from wheel
   ```
