# Process Improvement using Data

Source repository for the open-access book *Process Improvement using Data* by
Kevin Dunn. Actively written and updated since August 2010.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Read online](https://img.shields.io/badge/read-learnche.org%2Fpid-blue.svg)](https://learnche.org/pid)
[![Download PDF](https://img.shields.io/badge/download-PDF-red.svg)](https://learnche.org/pid/PID.pdf?2026-05-19)
[![Build status](https://img.shields.io/github/actions/workflow/status/kgdunn/pid-book/build-deploy.yml?branch=main&label=build)](https://github.com/kgdunn/pid-book/actions/workflows/build-deploy.yml)
[![Last commit](https://img.shields.io/github/last-commit/kgdunn/pid-book.svg)](https://github.com/kgdunn/pid-book/commits)
[![Issues](https://img.shields.io/github/issues/kgdunn/pid-book.svg)](https://github.com/kgdunn/pid-book/issues)

## Read the book

The book is free to read online and free to download. You do **not** need this
repository to read it:

- **Read online:** **<https://learnche.org/pid>**
- **Download the PDF:** **[PID.pdf](https://learnche.org/pid/PID.pdf?2026-05-19)**

This repository holds the book's source. It is here for people who want to
report a problem, contribute a correction, or build the book themselves — see
[Contributing](#contributing) below.

## What the book is about

*Process Improvement using Data* teaches the statistical methods that engineers
and scientists use to learn from process data — how to **visualize** it,
**model** it, **monitor** it, and use it to **improve** products and processes.
It is practical and example-driven: most concepts are introduced through a
real dataset and a worked analysis rather than through theory alone.

It suits an upper-undergraduate or introductory-graduate course, and it works
equally well for self-study by practitioners who want to put these tools to use
on their own data.

| Chapter | Topic |
|---|---|
| 1 | Data visualization |
| 2 | Univariate review (probability, distributions, confidence intervals, hypothesis tests) |
| 3 | Process monitoring (Shewhart, CUSUM, EWMA charts) |
| 4 | Least-squares modelling (linear and multiple regression) |
| 5 | Design and analysis of experiments (DOE) |
| 6 | Latent variable modelling (PCA, PLS, batch data analysis) |
| 7 | Product development and product improvement |

The full table of contents lives in [`contents.rst`](contents.rst).

## For instructors

You're welcome to use this book — and the course materials below — for your
own teaching. Everything is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), so you can
share, adapt, and even commercialize derivative work as long as you attribute
the original and license the result under the same terms. No permission
needed.

The book has been adopted at other universities (undergraduate and graduate)
and used inside companies as an internal training manual.

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

**Teaching at a company?** Get in touch via the
[contact page](https://learnche.org/4C3/Statistics_for_Engineering:About) for
additional slides, worksheets, and tips.

Questions, comments, or "how did you make that figure?" enquiries are all
welcome through the same contact link.

## Contributing

Contributions, corrections, and exercises are welcome. The book has been
improved continuously since 2010 thanks to readers like you. The fastest
channels:

1. **Open an [issue](https://github.com/kgdunn/pid-book/issues)** for typos,
   technical errors, broken links, or build problems.
2. **Open a pull request** for content changes.
3. **Long-form feedback**, course adoption stories, and exercise contributions
   can also go through [this Google Form](https://docs.google.com/forms/d/1IpO-bvJwQwhK64eid4YXwJBvGxN5cfyYDv81G-YgWrM/viewform).

[CONTRIBUTING.md](CONTRIBUTING.md) has everything a contributor needs: the
contribution workflow, how to build the book locally, the repository layout,
the RST style notes, and how the book is published.

## License and citation

The book is licensed under the
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
license. You are free to copy, adapt, and redistribute it — including for
courses you teach — provided you attribute the original author and license
your derivative work under the same terms.

Suggested attribution:

> Dunn, K. G. (2010–2026). *Process Improvement using Data.* learnche.org/pid (CC BY-SA 4.0).

Machine-readable citation metadata is available in
[`CITATION.cff`](CITATION.cff).

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
