# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
# Add "-W" to cause warnings to turn into errors.
SPHINXOPTS    = -E -j auto
RELAXOPTS     = -E
SPHINXBUILD   = uv run sphinx-build
PAPER         =
BUILDDIR      = _build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
ALLRELAXEDOPTS  =  -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(RELAXOPTS) .

.PHONY: help setup clean clean-all html dirhtml singlehtml pickle json htmlhelp epub latex latexpdf text gettext linkcheck serve pre-commit-install pre-commit-run

.DEFAULT_GOAL := latexpdf

help:
	@echo "Process Improvement using Data — make targets"
	@echo
	@echo "Primary:"
	@echo "  html       Build the HTML book (also runs Pagefind for search)"
	@echo "  latexpdf   Build the PDF — needs LaTeX (this is the default target)"
	@echo "  latex      Build the LaTeX sources only, without running pdflatex"
	@echo "  epub       Build the EPUB"
	@echo "  text       Build the plain-text output"
	@echo
	@echo "Development:"
	@echo "  setup               Install uv and sync dependencies"
	@echo "  serve               Serve the built HTML at http://localhost:8080"
	@echo "  linkcheck           Check all external links"
	@echo "  pre-commit-install  Install the pre-commit git hook"
	@echo "  pre-commit-run      Run every pre-commit hook over the tree"
	@echo "  clean               Remove build artifacts"
	@echo "  clean-all           Also remove the venv and lockfile"
	@echo
	@echo "Set PAPER=a4 or PAPER=letter for the LaTeX targets."



clean: 		## Remove build artifacts
	rm -rf $(BUILDDIR)
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-all: clean	## Also remove the virtualenv and lockfile (forces a re-resolve next setup)
	rm -rf .venv/ lib/ lib64/ bin/
	rm -f uv.lock

setup:		## Bootstrap the toolchain: install uv, create .venv, sync deps from pyproject.toml + uv.lock
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv python install
	uv sync
	@command -v latexmk >/dev/null 2>&1 || { \
		echo "WARNING: latexmk not found. 'make latexpdf' will not work."; \
		echo "Install it with:  sudo apt-get install texlive-full latexmk"; \
		echo "  (or on Fedora:  sudo dnf install texlive-scheme-full latexmk)"; \
	}

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	cp -R $(BUILDDIR)/text/* $(BUILDDIR)/html/_sources/
	# With html_file_suffix="" Sphinx emits extensionless pages that
	# Pagefind's default **/*.html glob misses. --glob "**" indexes all
	# files; Pagefind skips non-HTML content automatically. Sphinx's own
	# searchindex.js remains the primary search.
	npx -y pagefind --site $(BUILDDIR)/html --glob "**"
	# index.html is the web-server directory-index convention so that
	# https://learnche.org/pid/ auto-redirects to /pid/contents.
	printf '<!DOCTYPE html>\n<html><head><meta http-equiv="refresh" content="0; url=contents"><link rel="canonical" href="contents"></head><body><a href="contents">Redirecting to contents…</a></body></html>\n' > $(BUILDDIR)/html/index.html
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
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	cp preface/*.png $(BUILDDIR)/latex
	cp preface/*.jpg $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf:
	@command -v latexmk >/dev/null 2>&1 || { \
		echo "ERROR: latexmk not found."; \
		echo "Install it with:  sudo apt-get install texlive-full latexmk"; \
		echo "  (or on Fedora:  sudo dnf install texlive-scheme-full latexmk)"; \
		exit 1; \
	}
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	cp preface/*.png $(BUILDDIR)/latex
	cp preface/*.jpg $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(BUILDDIR)/latex/PID.pdf; \
	elif command -v open >/dev/null 2>&1; then \
		open $(BUILDDIR)/latex/PID.pdf; \
	else \
		echo "PDF built at $(BUILDDIR)/latex/PID.pdf (no opener found)."; \
	fi

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

serve:
	uvx python start_server.py
	#python -m http.server 8080 --directory _build/html/

pre-commit-install:	## Install the pre-commit git hook
	uvx pre-commit install

pre-commit-run:		## Run every pre-commit hook against the whole tree
	uvx pre-commit run --all-files
