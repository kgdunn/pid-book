"""Sphinx configuration file for Process Improvement Using Data book.

This configuration file was originally created in 2010 and has been
modernized to use current best practices (2024+).
"""

import os
import sys
import datetime
import subprocess

from sphinx.highlighting import PygmentsBridge
from pygments.formatters.latex import LatexFormatter

sys.path.append(os.getcwd())
sys.path.insert(0, os.path.abspath("."))

# Minimum Sphinx version required
needs_sphinx = "5.0"

# =============================================================================
# Extensions Configuration
# =============================================================================

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinxcontrib.jquery",
    "my-extensions.youtube",
    "my-extensions.q-and-a",
    "my-extensions.datacamplite",
]

# JQuery configuration
jquery_use_sri = False

# Q&A extension: Set to True to create full solutions in the book
q_and_a_override = False


# =============================================================================
# Project Information
# =============================================================================

templates_path = ["_templates"]
source_suffix = {".rst": "restructuredtext"}
root_doc = "contents"  # Modern name for master_doc

the_year = str(datetime.datetime.now().year)
project = "Process Improvement Using Data"
author = "Kevin Dunn"
copyright = f"2010-{the_year} {author}"
today_fmt = "%d %B %Y"

# Get the Git revision number as version
try:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )
    release = result.stdout.strip()[:7]
except (subprocess.CalledProcessError, FileNotFoundError):
    release = "unknown"

version = release  # Short version

# Build configuration
nitpicky = True  # Emit warnings for all missing references
language = "en"
exclude_patterns = ["_build", ".hg", "ext", "DELETE", ".venv", "**/.ipynb_checkpoints"]
pygments_style = "sphinx"
add_function_parentheses = True

# These substitutions apply to every RST file
rst_prolog = """
.. meta::
   :http-equiv=X-UA-Compatible: IE=EmulateIE7
"""

rst_epilog = r"""
.. |x| replace:: :math:`\mathrm{x}`
.. |y| replace:: :math:`\mathrm{y}`
.. |z| replace:: :math:`\mathrm{z}`
.. |n| replace:: :math:`n`
.. |b0| replace:: :math:`b_0`
.. |b1| replace:: :math:`b_1`
.. |-| replace:: :math:`-`
.. |+| replace:: :math:`+`
.. |t| replace:: :math:`\mathbf{t}`
.. |T| replace:: :math:`\mathbf{T}`
.. |X| replace:: :math:`\mathbf{X}`
.. |Xraw| replace:: :math:`\mathbf{X}_\text{raw}`
.. |P| replace:: :math:`\mathbf{P}`
.. |p1| replace:: :math:`\mathbf{p}_1`
.. |T2| replace:: :math:`T^2`
.. |R| replace:: :math:`\mathbf{R}`
.. |U| replace:: :math:`\mathbf{U}`
.. |Y| replace:: :math:`\mathbf{Y}`
.. |W| replace:: :math:`\mathbf{W}`
.. |Z| replace:: :math:`\mathbf{Z}`
.. |Q2| replace:: :math:`Q^2`
.. |A| replace:: :math:`A`
.. |K| replace:: :math:`K`
.. |M| replace:: :math:`M`
.. |Cpk| replace:: C\ :sub:`pk`
.. |xdb| replace:: :math:`\overline{\overline{x}}`
"""

# =============================================================================
# HTML Output Configuration
# =============================================================================

html_theme = "sphinx_rtd_theme_kgdmod"
html_theme_path = ["."]
html_title = "Process Improvement using Data"
html_logo = "preface/textbook-logo-no-text-lowres.jpg"
html_favicon = "sphinx_rtd_theme_kgdmod/static/media/favicon.ico"
html_last_updated_fmt = "%d %B %Y"
html_use_index = True
html_show_sourcelink = False
html_copy_source = True
html_search_language = "en"
html_show_sphinx = False
html_show_copyright = True
html_permalinks = True
html_permalinks_icon = "¶"
html_file_suffix = ""
html_link_suffix = ""
html_secnumber_suffix = r". "


# =============================================================================
# Link Checking Configuration
# =============================================================================

linkcheck_ignore = [
    r"http://localhost:\d+/",
    r"http://dx.doi.org/.+",
    r"http://www.jstor.org/pss/.+",
    r"http://books.google.com/.+",
]
linkcheck_timeout = 20
linkcheck_workers = 10
linkcheck_anchors = True

# =============================================================================
# LaTeX/PDF Output Configuration
# =============================================================================

latex_documents = [
    (
        "contents",
        "PID.tex",
        "Process Improvement Using Data",
        author,
        "manual",
        True,
    ),
]

latex_logo = html_logo
latex_show_pagerefs = True
latex_use_parts = False
latex_show_urls = "footnote"


# Custom LaTeX formatter for code blocks
class CustomLatexFormatter(LatexFormatter):
    """Customized LaTeX formatter with smaller code font size."""

    def __init__(self, **options):
        super().__init__(**options)
        self.verboptions = r"formatcom=\footnotesize,frame=lines"


PygmentsBridge.latex_formatter = CustomLatexFormatter


# Commands that go at the TOC section
_TABLE_OF_CONTENTS = r"""
% ==== BEGIN CUSTOMIZED TOC ====

~\vfill
\thispagestyle{empty}
Copyright \copyright\ 2010 to \the\year\ Kevin G. Dunn

% Sphinx has decided to set this to "-2" in one of the newer versions.
% Set it "+1", which is what we are looking for
% Apparently cleared up in Sphinx 1.3.5
%\setcounter{tocdepth}{+1}

%\pagenumbering{gobble}
\tableofcontents
% \pagenumbering{gobble}
%\thispagestyle{empty}
%\pagenumbering{gobble}
\addtocontents{toc}{\protect\thispagestyle{empty}}
%\pagenumbering{gobble}
% ==== END OF CUSTOMIZED TOC ====

"""

_PREAMBLE = r"""
% ==== BEGIN CUSTOMIZED PREAMBLE ====
\usepackage{float}
\usepackage{cancel}  % to get cancelled terms
\usepackage{upquote} % to avoid quotation marks from being mangled
\usepackage{textpos} % get YouTube links outside the margin. Tthe package is in "relative" mode
\renewcommand{\PYGZsq}{TO AVOID ERROR MESSAGE}


\usepackage[]{geometry}
%\geometry{left=1.0in,width=6.5in,top=0.75in,height=9.25in,nohead,footskip=0.5in,portrait}
 \geometry{left=1.0in,width=6.5in,top=1.00in,height=9.25in,       footskip=0.5in,portrait}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=black,
    filecolor=black,
    urlcolor=blue
}
%\fvset{frame=single,xleftmargin=9pt,numbersep=4pt}

% Nicer URLs
\usepackage{url}
\makeatletter
\def\Url@twoslashes{\mathchar`\/\@ifnextchar/{\kern-.2em}{}}
\g@addto@macro\UrlSpecials{\do\/{\Url@twoslashes}}
\makeatother



\renewcommand{\sectionmark}[1]%
{\markright{\MakeUppercase{\thesection.\ #1}}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyhf{}
\fancyfoot[C]{\thepage}
\fancyhead[RO]{}
\fancyhead[LE]{}

\fancypagestyle{plain}{
  \fancyhf{} % empty header and footer
  \renewcommand{\headrulewidth}{0pt} % ho header line
  \renewcommand{\footrulewidth}{0pt}% not footer line
  \fancyfoot[C]{\thepage}% like fancy style
}

\makeatletter
\def\@subtitle{\relax}
\newcommand{\subtitle}[1]{\gdef\@subtitle{#1}}
\makeatother



\makeatletter
\renewcommand{\releasename}{Version}
\renewcommand{\maketitle}{%
  \begin{titlepage}%
    \let\footnotesize\small
    \let\footnoterule\relax
    \rule{\textwidth}{1pt}%

    \begin{flushright}%
      % \sphinxlogo% Don't want logo here, and not this size. Manually placed it a few lines down.
      {\rm\Huge\py@HeaderFamily \@title \par}%
      \vfill
      {\LARGE\py@HeaderFamily \@author \par}
      \vfill\vfill
      \includegraphics[scale=0.35]{textbook-logo-no-text.jpg}
      \\
      {\large
       \@date \par
       \vfill
       \py@authoraddress \par
       \vfill
       {\Large\py@HeaderFamily Version: \py@release\releaseinfo \par}
      }%
    \end{flushright}%\par
    \@thanks
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \let\thanks\relax\let\maketitle\relax
  %\gdef\@thanks{}\gdef\@author{}\gdef\@title{}
}
\makeatother



\fancypagestyle{normal}{
  \fancyhf{}
  \fancyfoot[LE,RO]{{\py@HeaderFamily\thepage}}
  \fancyfoot[LO]{{\py@HeaderFamily\nouppercase{\rightmark}}}
  \fancyfoot[RE]{{\py@HeaderFamily\nouppercase{\leftmark}}}
  \fancyhead[LE,RO]{{\py@HeaderFamily \@title, \py@release}}
  \renewcommand{\headrulewidth}{0.4pt}
  \renewcommand{\footrulewidth}{0.4pt}
}

\makeatletter
  % Use \pagestyle{normal} as the primary pagestyle for text.
  \fancypagestyle{normal}{
    \fancyhf{}
    \fancyfoot[LE,RO]{{\py@HeaderFamily\thepage}}
    \fancyfoot[LO]{{\py@HeaderFamily\nouppercase{\rightmark}}}
    \fancyfoot[RE]{{\py@HeaderFamily\nouppercase{\leftmark}}}
    \fancyhead[LE]{{\py@HeaderFamily \@title}} % before: \py@HeaderFamily \@title, \py@release
    \fancyhead[RO]{{\py@HeaderFamily \py@release}} % before: \py@HeaderFamily \@title, \py@release
    \renewcommand{\headrulewidth}{0.4pt}
    \renewcommand{\footrulewidth}{0.4pt}
  }
  % Update the plain style so we get the page number & footer line,
  % but not a chapter or section title.  This is to keep the first
  % page of a chapter and the blank page between chapters `clean.'
  \fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[LE,RO]{{\py@HeaderFamily\thepage}}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0.4pt}
  }

  \definecolor{VerbatimColor}{rgb}{1,1,1}
  \definecolor{VerbatimBorderColor}{rgb}{1,1,1}


  % Better style: use ragged right (based on https://tufte-latex.github.io/tufte-latex/)
  \raggedright
  % \RaggedRight allows hyphenation
  \RequirePackage{ragged2e}
  \setlength{\RaggedRightRightskip}{\z@ plus 0.08\hsize}


  % Set the font sizes and baselines to match Tufte's books
  \renewcommand\normalsize{%
     \@setfontsize\normalsize\@xpt{14}%
     \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
     \abovedisplayshortskip \z@ \@plus3\p@
     \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
     \belowdisplayskip \abovedisplayskip
     \let\@listi\@listI}
  \normalbaselineskip=14pt
  \normalsize
  \renewcommand\small{%
     \@setfontsize\small\@ixpt{12}%
     \abovedisplayskip 8.5\p@ \@plus3\p@ \@minus4\p@
     \abovedisplayshortskip \z@ \@plus2\p@
     \belowdisplayshortskip 4\p@ \@plus2\p@ \@minus2\p@
     \def\@listi{\leftmargin\leftmargini
                 \topsep 4\p@ \@plus2\p@ \@minus2\p@
                 \parsep 2\p@ \@plus\p@ \@minus\p@
                 \itemsep \parsep}%
     \belowdisplayskip \abovedisplayskip
  }
  \renewcommand\footnotesize{%
     \@setfontsize\footnotesize\@viiipt{10}%
     \abovedisplayskip 6\p@ \@plus2\p@ \@minus4\p@
     \abovedisplayshortskip \z@ \@plus\p@
     \belowdisplayshortskip 3\p@ \@plus\p@ \@minus2\p@
     \def\@listi{\leftmargin\leftmargini
                 \topsep 3\p@ \@plus\p@ \@minus\p@
                 \parsep 2\p@ \@plus\p@ \@minus\p@
                 \itemsep \parsep}%
     \belowdisplayskip \abovedisplayskip
  }
  \renewcommand\scriptsize{\@setfontsize\scriptsize\@viipt\@viiipt}
  \renewcommand\tiny{\@setfontsize\tiny\@vpt\@vipt}
  \renewcommand\large{\@setfontsize\large\@xipt{15}}
  \renewcommand\Large{\@setfontsize\Large\@xiipt{16}}
  \renewcommand\LARGE{\@setfontsize\LARGE\@xivpt{18}}
  \renewcommand\huge{\@setfontsize\huge\@xxpt{30}}
  \renewcommand\Huge{\@setfontsize\Huge{24}{36}}

  \setlength\leftmargini   {1pc}
  \setlength\leftmarginii  {1pc}
  \setlength\leftmarginiii {1pc}
  \setlength\leftmarginiv  {1pc}
  \setlength\leftmarginv   {1pc}
  \setlength\leftmarginvi  {1pc}
  \setlength\labelsep      {.5pc}
  \setlength\labelwidth    {\leftmargini}
  \addtolength\labelwidth{-\labelsep}


\makeatother
% ==== END OF CUSTOMIZED PREAMBLE ====
"""

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "fontpkg": r"\usepackage{palatino}",
    "preamble": _PREAMBLE,
    "figure_align": "H",
    "fncychap": r"\usepackage[Glenn]{fncychap}",
    "tableofcontents": _TABLE_OF_CONTENTS,
    "inputenc": r"\usepackage[utf8]{inputenc}",
    "fontenc": r"\usepackage[T1]{fontenc}",
    "printindex": r"\printindex",
    "releasename": "",
}

# =============================================================================
# EPUB Output Configuration
# =============================================================================

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_language = "en"
epub_basename = "PID"
epub_theme = "epub"
epub_tocdepth = 3
epub_use_index = True
