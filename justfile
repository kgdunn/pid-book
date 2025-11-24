# Justfile for Process Improvement Using Data book
# Modern command runner - https://github.com/casey/just
# Install with: curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin
# Or with package managers: brew install just, cargo install just, etc.

# Default recipe to display help information
default:
    @just --list

# Set up Python environment with uv
install:
    @echo "Setting up Python environment..."
    @command -v uv >/dev/null 2>&1 || (echo "Installing uv..." && curl -LsSf https://astral.sh/uv/install.sh | sh)
    uv sync --all-extras
    @echo "✓ Environment setup complete!"

# Alias for install
setup: install

# Install pre-commit hooks
pre-commit-install: install
    @echo "Installing pre-commit hooks..."
    uv run pre-commit install
    @echo "✓ Pre-commit hooks installed!"

# Run pre-commit on all files
pre-commit:
    @echo "Running pre-commit checks..."
    uv run pre-commit run --all-files

# Build HTML documentation
html:
    @echo "Building HTML..."
    sphinx-build -b html -E -j auto . _build/html
    sphinx-build -b text -E -j auto . _build/text
    cp -R _build/text/* _build/html/_sources/
    @echo "✓ HTML build complete: _build/html/index.html"

# Build PDF documentation
pdf:
    @echo "Building PDF..."
    sphinx-build -b latex -E -j auto . _build/latex
    cp preface/*.png _build/latex/
    cp preface/*.jpg _build/latex/
    cd _build/latex && make all-pdf
    @echo "✓ PDF build complete: _build/latex/PID.pdf"

# Build EPUB e-book
epub:
    @echo "Building EPUB..."
    sphinx-build -b epub -E -j auto . _build/epub
    @echo "✓ EPUB build complete: _build/epub/PID.epub"

# Build all formats (HTML, PDF, EPUB)
all: html pdf epub
    @echo ""
    @echo "✓ All builds complete!"
    @echo "  HTML: _build/html/index.html"
    @echo "  PDF:  _build/latex/PID.pdf"
    @echo "  EPUB: _build/epub/PID.epub"

# Check all external links
linkcheck:
    @echo "Checking links..."
    sphinx-build -b linkcheck -E . _build/linkcheck
    @echo "✓ Link check complete: see _build/linkcheck/output.txt"

# Remove build artifacts
clean:
    @echo "Cleaning build artifacts..."
    rm -rf _build
    rm -rf *.pyc
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -fr {} +
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.egg' -exec rm -f {} +
    @echo "✓ Clean complete!"

# Remove build artifacts AND virtual environment
clean-all: clean
    @echo "Removing virtual environment..."
    rm -f uv.lock
    rm -rf .venv/
    rm -rf lib/
    rm -rf lib64/
    rm -rf bin/
    @echo "✓ Full clean complete!"

# Start local web server to view HTML build
serve:
    @echo "Starting local server at http://localhost:8080"
    @echo "Press Ctrl+C to stop"
    uv run python start_server.py

# Open HTML build in default browser
open-html:
    @if command -v xdg-open >/dev/null 2>&1; then \
        xdg-open _build/html/index.html; \
    elif command -v open >/dev/null 2>&1; then \
        open _build/html/index.html; \
    else \
        echo "Please open _build/html/index.html manually"; \
    fi

# Open PDF in default viewer
open-pdf:
    @if command -v xdg-open >/dev/null 2>&1; then \
        xdg-open _build/latex/PID.pdf; \
    elif command -v open >/dev/null 2>&1; then \
        open _build/latex/PID.pdf; \
    else \
        echo "Please open _build/latex/PID.pdf manually"; \
    fi

# Run a quick build cycle (HTML only)
quick: html
    @echo "✓ Quick build complete!"

# Full rebuild from scratch
rebuild: clean all
    @echo "✓ Full rebuild complete!"

# Watch for changes and rebuild HTML (requires entr)
watch:
    @if ! command -v entr >/dev/null 2>&1; then \
        echo "Error: entr is not installed. Install it with:"; \
        echo "  Ubuntu/Debian: sudo apt-get install entr"; \
        echo "  macOS: brew install entr"; \
        exit 1; \
    fi
    @echo "Watching for changes (press Ctrl+C to stop)..."
    find . -name '*.rst' -o -name '*.py' | entr just html
