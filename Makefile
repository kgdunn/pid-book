# Makefile for Sphinx documentation
# Modernized build system for "Process Improvement Using Data"

# You can set these variables from the command line.
# Add "-W" to turn warnings into errors for strict builds
SPHINXOPTS    = -E -j auto
RELAXOPTS     = -E
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build
UV            = uv

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
ALLRELAXEDOPTS  =  -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(RELAXOPTS) .

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext whoosh install setup all pre-commit-install pre-commit-run

.DEFAULT_GOAL := all

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "Primary targets:"
	@echo "  all               to build HTML, PDF, and EPUB (default)"
	@echo "  install           to set up the Python environment with uv"
	@echo "  html              to make standalone HTML files"
	@echo "  latexpdf          to make LaTeX files and run them through pdflatex"
	@echo "  epub              to make an EPUB e-book"
	@echo "  clean             to remove build artifacts"
	@echo ""
	@echo "Development targets:"
	@echo "  pre-commit-install  to install pre-commit hooks"
	@echo "  pre-commit-run      to run pre-commit on all files"
	@echo "  linkcheck           to check all external links for integrity"
	@echo "  serve               to start a local web server for the HTML build"
	@echo ""
	@echo "Additional targets:"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  text       to make text files"
	@echo ""
	@echo "Environment variables:"
	@echo "  PAPER=a4 or PAPER=letter  to set paper size for PDF"



install:  ## Set up Python environment with uv
	@echo "Setting up Python environment..."
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	$(UV) sync --all-extras
	@echo "Environment setup complete!"

setup: install  ## Alias for install

pre-commit-install: install  ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	$(UV) run pre-commit install
	@echo "Pre-commit hooks installed!"

pre-commit-run:  ## Run pre-commit on all files
	@echo "Running pre-commit checks..."
	$(UV) run pre-commit run --all-files

clean:  ## Remove build artifacts
	@echo "Cleaning build artifacts..."
	rm -rf $(BUILDDIR)
	rm -rf *.pyc
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	@echo "Clean complete!"

clean-all: clean  ## Remove build artifacts AND virtual environment
	@echo "Removing virtual environment..."
	rm -f uv.lock
	rm -rf .venv/
	rm -rf lib/
	rm -rf lib64/
	rm -rf bin/
	@echo "Full clean complete!"



html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	cp -R $(BUILDDIR)/text/* $(BUILDDIR)/html/_sources/
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

epub:
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The EPUB file is in $(BUILDDIR)/epub/PID.epub"

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	cp preface/*.png $(BUILDDIR)/latex
	cp preface/*.jpg $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	cp preface/*.png $(BUILDDIR)/latex
	cp preface/*.jpg $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex/PID.pdf"

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

gettext:
	$(SPHINXBUILD) -b gettext $(ALLSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLRELAXEDOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

all: html latexpdf epub  ## Build all formats (HTML, PDF, EPUB)
	@echo
	@echo "All builds complete!"
	@echo "  HTML: $(BUILDDIR)/html/index.html"
	@echo "  PDF:  $(BUILDDIR)/latex/PID.pdf"
	@echo "  EPUB: $(BUILDDIR)/epub/PID.epub"

serve:  ## Start a local web server to view HTML build
	@echo "Starting local server at http://localhost:8080"
	@echo "Press Ctrl+C to stop"
	$(UV) run python start_server.py

open-html:  ## Open the HTML build in default browser
	@command -v xdg-open >/dev/null 2>&1 && xdg-open $(BUILDDIR)/html/index.html || \
	command -v open >/dev/null 2>&1 && open $(BUILDDIR)/html/index.html || \
	echo "Please open $(BUILDDIR)/html/index.html manually"

open-pdf:  ## Open the PDF in default viewer
	@command -v xdg-open >/dev/null 2>&1 && xdg-open $(BUILDDIR)/latex/PID.pdf || \
	command -v open >/dev/null 2>&1 && open $(BUILDDIR)/latex/PID.pdf || \
	echo "Please open $(BUILDDIR)/latex/PID.pdf manually"

