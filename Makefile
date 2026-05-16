# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
# Add "-W" to cause warnings to turn into errors.
SPHINXOPTS    = -E -j auto
RELAXOPTS     = -E
SPHINXBUILD   = uv run sphinx-build
PAPER         =
BUILDDIR      = _build

# Theme used by `make theme-pdf`: tufte | academic | business
THEME         ?= tufte

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
ALLRELAXEDOPTS  =  -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(RELAXOPTS) .

.PHONY: help setup clean distclean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext whoosh theme-pdf theme-pdf-all

.DEFAULT_GOAL := latexpdf

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  htmlhelp   to make HTML files and a HTML help project"
	@echo "  qthelp     to make HTML files and a qthelp project"
	@echo "  devhelp    to make HTML files and a Devhelp project"
	@echo "  epub       to make an epub"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  text       to make text files"
	@echo "  gettext    to make PO message catalogs"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  theme-pdf  to build a carved-off PDF sample (preface + ch.3)"
	@echo "             with THEME=tufte|academic|business|business-ragged"
	@echo "  theme-pdf-all  to build every theme sample"



clean: 		## Remove build artifacts
	rm -rf $(BUILDDIR)
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

distclean: clean	## Also remove the virtualenv and lockfile (forces a re-resolve next setup)
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
	make -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(BUILDDIR)/latex/PID.pdf; \
	elif command -v open >/dev/null 2>&1; then \
		open $(BUILDDIR)/latex/PID.pdf; \
	else \
		echo "PDF built at $(BUILDDIR)/latex/PID.pdf (no opener found)."; \
	fi

# PDF theme comparison harness. Builds a small carved-off sample — the
# preface plus the process-monitoring chapter — with one alternative LaTeX
# theme, so several PDF designs can be compared without recompiling the whole
# book. The theme machinery lives in conf.py, gated on PID_PDF_THEME.
# Cross-references into the chapters left out of the sample render as plain
# text; that is expected for a layout preview.
theme-pdf:	## Build a PDF sample with THEME=tufte|academic|business|business-ragged
	@case "$(THEME)" in tufte|academic|business|business-ragged) ;; *) \
		echo "ERROR: THEME must be tufte, academic, business or business-ragged (got '$(THEME)')."; \
		exit 1;; esac
	@command -v latexmk >/dev/null 2>&1 || { \
		echo "ERROR: latexmk not found. See 'make setup'."; \
		exit 1; \
	}
	PID_PDF_THEME=$(THEME) $(SPHINXBUILD) -b latex $(SPHINXOPTS) \
		-d $(BUILDDIR)/theme-doctrees . $(BUILDDIR)/theme-$(THEME)
	cp preface/*.png $(BUILDDIR)/theme-$(THEME)
	cp preface/*.jpg $(BUILDDIR)/theme-$(THEME)
	@echo "Running LaTeX files through pdflatex..."
	make -C $(BUILDDIR)/theme-$(THEME) all-pdf
	@echo
	@echo "Theme sample: $(BUILDDIR)/theme-$(THEME)/PID-sample-$(THEME).pdf"

theme-pdf-all:	## Build every theme sample for side-by-side comparison
	$(MAKE) theme-pdf THEME=tufte
	$(MAKE) theme-pdf THEME=academic
	$(MAKE) theme-pdf THEME=business
	$(MAKE) theme-pdf THEME=business-ragged
	@echo
	@echo "Theme samples ready:"
	@echo "  $(BUILDDIR)/theme-tufte/PID-sample-tufte.pdf"
	@echo "  $(BUILDDIR)/theme-academic/PID-sample-academic.pdf"
	@echo "  $(BUILDDIR)/theme-business/PID-sample-business.pdf"
	@echo "  $(BUILDDIR)/theme-business-ragged/PID-sample-business-ragged.pdf"

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

