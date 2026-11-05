"""Link previews, the landing page's schema.org record and the sitemap (my-extensions/social_meta.py).

These tags are invisible on the page: a preview that shows an aside instead of the page's
opening, a broken image link or an unescaped quote only shows up when someone shares a link.
The tests pin what is picked as the description, how it is shortened and escaped, and which
page gets which image and record.
"""

import importlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace

from docutils import nodes
from docutils.core import publish_doctree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
social_meta = importlib.import_module("my-extensions.social_meta")

OPENING = (
    "The CUSUM chart accumulates small deviations from the target, so it detects a shift in the "
    "mean sooner than a Shewhart chart does."
)


def doctree(rst: str) -> nodes.document:
    return publish_doctree(rst, settings_overrides={"report_level": 5})


def test_description_skips_asides_and_short_lines():
    page = doctree(
        f"""
Title
=====

.. note:: A note placed first is an aside, however long it is, and is not the page's opening.

See below.

{OPENING}
"""
    )
    assert social_meta.description(page) == OPENING


def test_description_reads_inline_maths_as_plain_text():
    page = doctree(
        "The limits sit at :math:`\\overline{x} \\pm 3\\sigma` on either side of the target, for "
        "subgroups of a fixed size."
    )
    assert social_meta.description(page).startswith("The limits sit at x ± 3σ on either side")


def test_description_of_a_page_without_prose_is_empty():
    assert social_meta.description(doctree(".. note:: Only an aside on this page.")) == ""


def test_shorten_cuts_at_a_word_and_marks_the_cut():
    text = "word " * 100
    short = social_meta.shorten(text, limit=50)
    assert len(short) <= 50
    assert short.endswith("word…")
    assert social_meta.shorten("Short enough.", limit=50) == "Short enough."


def test_meta_tags_escape_values_and_leave_out_empty_ones():
    tags = social_meta.meta_tags(
        title='Quotes " and <tags>',
        summary="A & B",
        url="https://example.org/pid/contents",
        image_url="",
        image_alt="",
        image_size=(2560, 1280),
        site_name="Book",
        page_type="website",
    )
    assert 'content="Quotes &quot; and &lt;tags&gt;"' in tags
    assert '<meta name="description" content="A &amp; B" />' in tags
    assert '<meta name="twitter:card" content="summary_large_image" />' in tags
    assert 'property="og:image"' not in tags  # no image given: no image tag, not an empty one


def test_json_ld_cannot_close_its_script_element():
    script = social_meta.json_ld({"name": "</script><b>"})
    body = script.split("\n", 1)[1].rsplit("</script>", 1)[0]
    assert "</" not in body
    assert json.loads(body) == {"name": "</script><b>"}


def test_sitemap_is_valid_xml_listing_every_url():
    urls = ["https://example.org/pid/contents", "https://example.org/pid/a?b=1&c=2"]
    root = ET.fromstring(social_meta.sitemap(urls))
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    assert [loc.text for loc in root.findall("s:url/s:loc", namespace)] == urls


def fake_app(builder="html", baseurl="https://example.org/pid/"):
    """The parts of a Sphinx application the extension reads."""
    config = SimpleNamespace(
        html_baseurl=baseurl,
        html_title="The Book",
        root_doc="contents",
        social_meta_image="_static/hero.png",
        social_meta_image_alt="The book's card",
        social_meta_image_size=(2560, 1280),
        social_meta_chapter_images={"monitoring": "_static/social/monitoring.png"},
        social_meta_description="A free book.",
        social_meta_jsonld={"@type": "Book", "name": "The Book"},
    )
    return SimpleNamespace(
        config=config,
        builder=SimpleNamespace(name=builder, get_target_uri=lambda docname: docname),
        env=SimpleNamespace(titles={"monitoring/index": nodes.title("", "Process Monitoring")}),
    )


def tags_for(app, pagename, page=None):
    context = {"title": "CUSUM <em>charts</em>", "metatags": ""}
    social_meta._add_tags(app, pagename, "page.html", context, page if page is not None else doctree(OPENING))
    return context["metatags"]


def test_a_chapter_page_shows_its_chapter_card_and_opening():
    tags = tags_for(fake_app(), "monitoring/cusum")
    assert 'property="og:image" content="https://example.org/pid/_static/social/monitoring.png"' in tags
    assert "Process Monitoring: an example from The Book" in tags
    assert f'property="og:description" content="{OPENING}"' in tags
    assert 'property="og:title" content="CUSUM charts | The Book"' in tags
    assert 'property="og:type" content="article"' in tags
    assert "application/ld+json" not in tags


def test_the_landing_page_has_the_fixed_description_and_the_record():
    tags = tags_for(fake_app(), "contents")
    assert 'property="og:image" content="https://example.org/pid/_static/hero.png"' in tags
    assert 'property="og:description" content="A free book."' in tags
    assert 'property="og:type" content="website"' in tags
    assert '"@type": "Book"' in tags


def test_a_page_outside_the_chapters_gets_the_book_card():
    tags = tags_for(fake_app(), "preface/index")
    assert 'property="og:image" content="https://example.org/pid/_static/hero.png"' in tags


def test_nothing_is_added_without_a_base_url_or_outside_html():
    assert tags_for(fake_app(baseurl=""), "monitoring/cusum") == ""
    assert tags_for(fake_app(builder="latex"), "monitoring/cusum") == ""
