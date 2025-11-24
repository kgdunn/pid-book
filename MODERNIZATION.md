# Build Toolchain Modernization

This document summarizes the modernization of the build toolchain for the "Process Improvement Using Data" book (November 2024).

## Overview

The build system has been modernized from its original 2010 setup to use current best practices and tools as of 2024. All core functionality (HTML and PDF generation) is preserved, with additional output formats and automation added.

## Key Improvements

### 1. Modernized Makefile

**Changes:**
- Separated environment setup (`make install`) from cleaning (`make clean`)
- Changed default target from `latexpdf` to `all` (builds HTML, PDF, and EPUB)
- Added `make all` to build all formats at once
- Uses `-j auto` for automatic parallel build optimization (was hardcoded `-j 5`)
- Cross-platform file opening with `open-html` and `open-pdf` targets
- Added `clean-all` target that also removes virtual environment
- Better help documentation with organized sections
- Uses `uv sync --all-extras` for proper dependency management

**New Targets:**
- `make all` - Build HTML, PDF, and EPUB (now the default)
- `make pre-commit-install` - Install pre-commit hooks
- `make pre-commit-run` - Run code quality checks
- `make open-html` - Open HTML in browser (cross-platform)
- `make open-pdf` - Open PDF in viewer (cross-platform)

### 2. Cleaned Up Sphinx Configuration (conf.py)

**Changes:**
- Removed 700+ lines of outdated comments and dead code
- Modernized imports and configuration patterns
- Used `root_doc` instead of deprecated `master_doc`
- Consolidated extensions configuration
- Improved git version extraction with modern `subprocess.run()`
- Better organized sections with clear headers
- Improved EPUB configuration
- Updated minimum Sphinx version to 5.0 (from 1.5)

### 3. Added EPUB Output Format

**What:**
- EPUB is now a standard output format alongside HTML and PDF
- Properly configured with metadata and settings
- Included in `make all` and CI/CD builds

**Why:**
- Modern e-readers and mobile devices
- Better accessibility
- Reflowable content for different screen sizes

### 4. GitHub Actions CI/CD

**File:** `.github/workflows/build-book.yml`

**Features:**
- Automatic builds on push and pull requests
- Parallel jobs for HTML, PDF, and EPUB
- Link checking (with failure allowed)
- Build artifacts available for download (30-90 day retention)
- Build summary in GitHub Actions UI
- Uses modern actions (checkout@v4, upload-artifact@v4)
- Caching for faster builds

### 5. Pre-commit Hooks

**Files:**
- `.pre-commit-config.yaml` - Pre-commit configuration
- `ruff.toml` - Python code quality settings (also in pyproject.toml)

**Hooks:**
- Trailing whitespace removal
- End-of-file fixing
- YAML/TOML validation
- Merge conflict detection
- Python code formatting with Ruff
- reStructuredText linting with rstcheck

**Usage:**
```bash
make pre-commit-install  # One-time setup
make pre-commit-run      # Manual run
# Hooks run automatically on git commit
```

### 6. Justfile (Modern Alternative to Make)

**File:** `justfile`

**What:**
- Modern command runner as an alternative to Make
- More intuitive syntax and better error messages
- All the same functionality as Makefile

**Features:**
- Same targets as Makefile with cleaner syntax
- `just watch` - Auto-rebuild on file changes (requires `entr`)
- `just quick` - Fast HTML-only build
- `just rebuild` - Full clean + rebuild
- Better user feedback with checkmarks and colors
- Built-in command listing with `just` or `just --list`

### 7. Enhanced Documentation

**Changes to README.md:**
- Comprehensive installation instructions for all platforms
- Quick start guide
- Both Make and Just command references
- Development workflow documentation
- CI/CD information
- Contributing guidelines
- Clear output locations

### 8. Updated Dependencies

**pyproject.toml:**
- Added `[project.optional-dependencies]` for development tools
- Added Ruff configuration
- Modern package metadata structure
- Development dependencies: pre-commit, ruff, rstcheck

## Build System Comparison

### Before (2010-2024)
```bash
make clean     # Reinstalled uv every time!
make html      # HTML only
make latexpdf  # PDF only
# No EPUB, no CI/CD, no code quality tools
```

### After (2024+)
```bash
make install   # One-time setup
make all       # HTML + PDF + EPUB
make serve     # Local preview
# With CI/CD, pre-commit hooks, and modern tooling
```

## Technical Details

### Parallel Builds
- Changed from `-j 5` to `-j auto` for optimal CPU usage
- Automatically uses all available cores

### Version Control Integration
- Git commit hash used as version identifier
- Properly extracted using modern subprocess API

### Cross-Platform Support
- Conditional logic for opening files (Linux/macOS/Windows)
- Platform-agnostic path handling
- LaTeX installation instructions for all platforms

### Dependency Management
- Uses `uv` for fast, reliable Python package management
- Lockfile (`uv.lock`) for reproducible builds
- Separate dev dependencies

## Migration Guide

### For Existing Users

If you've been using the old build system:

1. **Update your workflow:**
   ```bash
   git pull
   make install        # New: separate from clean
   make all           # New: builds all formats
   ```

2. **Optional: Install pre-commit hooks:**
   ```bash
   make pre-commit-install
   ```

3. **Optional: Try the modern alternative:**
   ```bash
   # Install just (optional)
   curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash

   # Use it
   just install
   just all
   ```

### Breaking Changes

**None!** The old commands still work:
- `make clean` still works (but doesn't reinstall uv)
- `make html` still works
- `make latexpdf` still works

The only change is the default target is now `all` instead of `latexpdf`.

## Testing

All changes have been validated:
- ✅ Makefile syntax verified
- ✅ Sphinx configuration loads correctly
- ✅ Version extraction works
- ✅ All new targets defined
- ✅ Documentation updated

## Future Enhancements

Possible future improvements:
- [ ] GitHub Pages deployment
- [ ] Automated releases on tags
- [ ] Multi-version documentation
- [ ] Search index optimization
- [ ] Mobile-optimized HTML theme option
- [ ] Docker container for consistent builds

## Credits

Modernization performed in November 2024 to bring the 10-year-old build system up to current best practices while maintaining backward compatibility.
