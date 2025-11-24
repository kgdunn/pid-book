# Process Improvement using Data

All the reStructuredText (RST) source files for the book with this title. The book has been actively written and updated since August 2010.


## Book website (HTML and PDF)

https://learnche.org/pid


## What you need to compile the book yourself

### Prerequisites

* Clone this repository
* Get the repository for all the figures: https://github.com/kgdunn/figures
* Python 3.12 or higher
* [uv](https://docs.astral.sh/uv/) - Modern Python package manager (installed automatically if using Make/Just)
* LaTeX distribution (for PDF generation):
  - **Linux**: `sudo apt-get install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended`
  - **macOS**: Install [MacTeX](https://www.tug.org/mactex/)
  - **Windows**: Install [MiKTeX](https://miktex.org/)
* Around 2GB of disk space for files, compiled documents, and illustrations
* A good text editor with RST syntax highlighting (VS Code, PyCharm, Sublime Text, etc.)

### Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/kgdunn/pid-book.git
cd pid-book

# 2. Set up the figures repository (symlink or clone inside this repo)
ln -s /path/to/figures ./figures
# OR clone it directly:
# git clone https://github.com/kgdunn/figures.git

# 3. Install dependencies (this will install uv if not present)
make install
# OR using just (modern alternative):
# just install

# 4. Build the book (HTML, PDF, and EPUB)
make all
# OR: just all
```

### Available Build Commands

#### Using Make (traditional)

```bash
make install        # Set up Python environment
make html           # Build HTML only (fastest)
make pdf            # Build PDF only
make epub           # Build EPUB only
make all            # Build all formats (default)
make clean          # Remove build artifacts
make serve          # Start local web server
make linkcheck      # Check all external links
```

#### Using Just (modern alternative)

[Just](https://github.com/casey/just) is a modern command runner that's more user-friendly than Make.

```bash
just install        # Set up Python environment
just html           # Build HTML only
just pdf            # Build PDF only
just epub           # Build EPUB e-book
just all            # Build all formats (default)
just clean          # Remove build artifacts
just serve          # Start local web server
just watch          # Auto-rebuild on file changes (requires entr)
```

Run `just` without arguments to see all available commands.

### Development Workflow

```bash
# Install pre-commit hooks for code quality
make pre-commit-install
# OR: just pre-commit-install

# Run pre-commit checks manually
make pre-commit-run
# OR: just pre-commit
```

### Build Output Locations

After building, you'll find the outputs in the `_build/` directory:

- **HTML**: `_build/html/index.html`
- **PDF**: `_build/latex/PID.pdf`
- **EPUB**: `_build/epub/PID.epub`

The HTML build is quick (1-2 minutes). The PDF build takes 5-10 minutes due to LaTeX compilation, cross-references, and index generation.


## Continuous Integration

This repository uses GitHub Actions to automatically build all formats (HTML, PDF, EPUB) on every push. The workflows:

- Build and validate all output formats
- Check for broken links
- Provide downloadable artifacts for each build

See [.github/workflows/build-book.yml](.github/workflows/build-book.yml) for details.

## Why would you want to compile it yourself?

Perhaps you would like to:
- Improve a section or fix errors
- Customize the book for a course you're teaching
- Add or remove topics
- Translate content
- Learn how Sphinx book publishing works

Whatever the reason, you're encouraged to do so! Everything is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license](https://creativecommons.org/licenses/by-sa/4.0/).

Your adaptations are allowed and encouraged, but must be distributed under the same or similar license conditions.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make pre-commit-run` or `just pre-commit` to check code quality
5. Submit a pull request

## Feedback

I'm always interested in feedback, comments, exercises, and contributions. You can:
- [Submit feedback via this form](https://docs.google.com/forms/d/1IpO-bvJwQwhK64eid4YXwJBvGxN5cfyYDv81G-YgWrM/viewform)
- [Open an issue on GitHub](https://github.com/kgdunn/pid-book/issues)
- Submit a pull request with improvements

Surprise me!