import pytest
import types

import reader.feed as feed_mod

class DummyFeed:
    def __init__(self, title="Test Feed", link="http://example.com"):
        self.title = title
        self.link = link

class DummyEntry:
    def __init__(self, title, content):
        self.title = title
        self.content = [{"value": content}]

class DummyParsed:
    def __init__(self, feed, entries):
        self.feed = feed
        self.entries = entries

@pytest.fixture(autouse=True)
def patch_feedparser(monkeypatch):
    dummy_feed = DummyFeed()
    dummy_entries = [
        DummyEntry("Article 1", "<p>Content 1</p>"),
        DummyEntry("Article 2", "<p>Content 2</p>")
    ]
    dummy_parsed = DummyParsed(dummy_feed, dummy_entries)
    monkeypatch.setattr(feed_mod, "feedparser", types.SimpleNamespace(parse=lambda url: dummy_parsed))
    # Patch html2text
    monkeypatch.setattr(feed_mod, "html2text", types.SimpleNamespace(html2text=lambda html: html.replace("<p>", "").replace("</p>", "")))
    # Patch reader.URL
    monkeypatch.setattr(feed_mod.reader, "URL", "http://dummy.url")
    # Clear cache
    feed_mod._get_feed.cache_clear()

def test_get_site():
    result = feed_mod.get_site()
    assert result == "Test Feed (http://example.com)"

def test_get_titles():
    titles = feed_mod.get_titles()
    assert titles == ["Article 1", "Article 2"]

def test_get_article_first():
    article = feed_mod.get_article(0)
    assert article.startswith("# Article 1")
    assert "Content 1" in article

def test_get_article_second():
    article = feed_mod.get_article(1)
    assert article.startswith("# Article 2")
    assert "Content 2" in article

def test_get_article_invalid_index():
    with pytest.raises(IndexError):
        feed_mod.get_article(5)