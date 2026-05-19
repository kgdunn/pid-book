# Process Improvement using Data

> *A free textbook on the statistics that engineers actually need.*
> Continuously written and refined in industry-facing classrooms since 2010.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20284934.svg)](https://doi.org/10.5281/zenodo.20284934)
[![Read online](https://img.shields.io/badge/read-learnche.org%2Fpid-blue.svg)](https://learnche.org/pid)
[![Download PDF](https://img.shields.io/badge/download-PDF-red.svg)](https://learnche.org/pid/PID.pdf)
[![Build status](https://img.shields.io/github/actions/workflow/status/kgdunn/pid-book/build-deploy.yml?branch=main&label=build)](https://github.com/kgdunn/pid-book/actions/workflows/build-deploy.yml)
[![Last commit](https://img.shields.io/github/last-commit/kgdunn/pid-book.svg)](https://github.com/kgdunn/pid-book/commits)
[![Issues](https://img.shields.io/github/issues/kgdunn/pid-book.svg)](https://github.com/kgdunn/pid-book/issues)

## Read the book

The book is free to read online and free to download. You do **not** need this
repository to read it:

- **Read online:** **<https://learnche.org/pid>**
- **Download the PDF:** **[PID.pdf](https://learnche.org/pid/PID.pdf)**

This repository holds the book's source. It is here for people who want to
report a problem, contribute a correction, or build the book themselves. See
[Contributing](#contributing) below.

---

## Why this book exists

There is no other free, coherent text that covers what engineers and scientists
actually do with process data (visualization, regression, designed
experiments, process monitoring, *and* multivariate / latent-variable methods)
in one volume.

Most textbooks pick one of those topics and go deep. Practitioners need all of
them, and need to see how they fit together, because real industrial problems
don't respect chapter boundaries. *Process Improvement using Data* was written
to fill that gap, and has been continuously refined in industry-facing
classrooms and in industrial practice since 2010.

It is suitable for upper-undergraduate or introductory-graduate courses, and
for self-study by working engineers and data scientists with a basic
statistics background.

## What's inside

| Chapter | Topic and what you'll take away |
|:-:|---|
| 1 | **Data visualization**: how to look at data before you model it. |
| 2 | **Univariate review**: probability, distributions, confidence intervals, and hypothesis tests, refreshed with engineering examples. |
| 3 | **Process monitoring**: Shewhart, CUSUM, and EWMA charts: the toolbox that catches problems before they leave the plant. |
| 4 | **Least-squares modelling**: linear and multiple regression, from first principles through honest diagnostics. |
| 5 | **Design and analysis of experiments**: factorial, fractional factorial, and response-surface designs; learning the most from the fewest runs. |
| 6 | **Latent variable modelling**: PCA, PLS, and batch data analysis: turning high-dimensional process data into actionable insight. |
| 7 | **Product development and product improvement**: combining DOE and latent variable methods to develop new products and improve existing ones. |

## Companion software: `process-improve`

Every method in this book has a worked, production-grade implementation in the
open-source Python package
[`process-improve`](https://github.com/kgdunn/process-improve). It provides PCA
and PLS with proper outlier diagnostics and prediction intervals, control
charts, designed experiments, and batch process monitoring. Install it with
`pip install process-improve` and run the exercises in any Jupyter notebook.

## Who's using this book

The book is adopted in university courses, cited in graduate research, and
used inside companies as internal training material. A few course adoptions:

- **Western University, Canada**: required text for the graduate course
  *CBE 9190: Advanced Statistical Process Analysis*.
- **UNSW Sydney, Australia**: recommended text for *CEIC6789: Data-driven
  Decision Making in Chemical Engineering and Food Science*.
- **McMaster University, Canada**: *IBEHS 4C03: Statistical Methods for
  Biomedical Engineering* is built on the book's foundations and adapts them
  into JupyterLab notebooks.

It is also cited in graduate theses and peer-reviewed research across a range
of fields, from chemometrics and semiconductor manufacturing to public health
and tribology.

Teaching or training with the book? Tell us via
[Discussions](https://github.com/kgdunn/pid-book/discussions). We'd be glad
to list your course here.

## For instructors

You're welcome to use this book, and the course materials below, for your
own teaching. Everything is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), so you can
share, adapt, and even commercialize derivative work as long as you attribute
the original and license the result under the same terms. No permission
needed.

Course materials live on the original
[Learning Chemical Engineering: Courses](https://learnche.org/4C3/Main_Page)
site:

- [Suggested course structure](https://learnche.org/4C3/Course_outlines)
- [PDF slides](https://learnche.org/4C3/Main_Page) covering every section of
  the book
- [Assignments (with solutions)](https://learnche.org/4C3/Assignments_from_prior_years)
- [Midterms / tests](https://learnche.org/4C3/Midterms_from_prior_years)
- [Final exams](https://learnche.org/4C3/Final_exams_from_prior_years)
- Projects for
  [response surface optimization](https://learnche.org/4C3/Response_surface_project_from_prior_years)
  and
  [design of experiments](https://learnche.org/4C3/Designed_experiments_projects_from_prior_years)
- A [tutorial to learn R](https://learnche.org/4C3/Software_tutorial)
- [Video recordings](https://learnche.org/4C3/Course_videos_and_audio_from_previous_years)
  of the course on YouTube
- [Sample datasets](https://openmv.net/) for assignments, tests, and practice

**Teaching at a company?** Ask via
[GitHub Discussions](https://github.com/kgdunn/pid-book/discussions) for
additional slides, worksheets, and tips.

Questions, comments, or "how did you make that figure?" enquiries are all
welcome there too.

## Contributing

Contributions, corrections, and exercises are welcome from anyone: students,
instructors, and practitioners alike. The book has been improved continuously
since 2010 thanks to readers like you. The fastest channels:

1. **Open an [issue](https://github.com/kgdunn/pid-book/issues)** for typos,
   technical errors, broken links, or build problems.
2. **Open a pull request** for content changes.
3. **Use [Discussions](https://github.com/kgdunn/pid-book/discussions)** for
   adoption stories, teaching ideas, and long-form feedback, or
   [this Google Form](https://docs.google.com/forms/d/1IpO-bvJwQwhK64eid4YXwJBvGxN5cfyYDv81G-YgWrM/viewform)
   if you prefer.

[CONTRIBUTING.md](CONTRIBUTING.md) has everything a contributor needs: the
contribution workflow, how to build the book locally, the repository layout,
the RST style notes, and how the book is published.

## License and citation

The book is licensed under the
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
license. You are free to copy, adapt, and redistribute it (including for
courses you teach) provided you attribute the original author and license
your derivative work under the same terms.

Suggested attribution:

> Dunn, K. G. (2010–2026). *Process Improvement using Data* (CC BY-SA 4.0). Zenodo. https://doi.org/10.5281/zenodo.20284934

Each tagged release is archived on Zenodo. The DOI above is the concept DOI:
it always resolves to the latest archived edition. Machine-readable citation
metadata, including the DOI, is in [`CITATION.cff`](CITATION.cff).

## Privacy and readership data

The HTML edition at <https://learnche.org/pid> records aggregate,
cookieless pageview and search-query signal so the maintainer can tell
which sections need attention. No cookies are set, no IP addresses are
stored, no third-party trackers are loaded, and the browser
*Do Not Track* setting is honoured. Self-hosted copies of this book do
not phone home.

The reader-facing summary lives at <https://learnche.org/pid/privacy>
(source: [`privacy.rst`](privacy.rst)). The aggregated dashboards (top
pages, per-page 90-day sparklines, search queries) are themselves
public at <https://learnche.org/_stats/> in keeping with the open
spirit of the book. Engineering and operations docs are under
[`docs/telemetry/`](docs/telemetry/).
