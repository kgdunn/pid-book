"""The checker serves openmv.net files from its cache, also when process-improve downloads them."""

import check_code_blocks
import pytest

_remote_data = pytest.importorskip("process_improve._remote_data")

URL = "https://openmv.net/file/sbr-batch-reactor.xlsx"


@pytest.fixture
def warm_cache(tmp_path, monkeypatch):
    """A cache that already holds the file, and a library downloader that must not be called for it."""
    monkeypatch.setattr(check_code_blocks, "CACHE_DIR", tmp_path)
    (tmp_path / "sbr-batch-reactor.xlsx").write_bytes(b"cached workbook")
    calls = []

    def network(url, timeout=None):
        calls.append(url)
        return b"from the network"

    monkeypatch.setattr(_remote_data, "fetch_remote_bytes", network)
    check_code_blocks._install_library_cache()
    return calls


def test_library_download_of_openmv_file_is_served_from_cache(warm_cache):
    assert _remote_data.fetch_remote_bytes(URL) == b"cached workbook"
    assert warm_cache == []


def test_other_urls_still_reach_the_library(warm_cache):
    assert _remote_data.fetch_remote_bytes("file:///tmp/local.csv") == b"from the network"
    assert warm_cache == ["file:///tmp/local.csv"]


def test_install_is_idempotent(warm_cache):
    hooked = _remote_data.fetch_remote_bytes
    check_code_blocks._install_library_cache()
    assert _remote_data.fetch_remote_bytes is hooked
