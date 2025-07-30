import pytest
from reader.viewer import show, show_list

def test_show_prints_article(capsys):
    article = "Test Article Content"
    show(article)
    captured = capsys.readouterr()
    assert captured.out.strip() == article

def test_show_list_prints_titles(capsys):
    site = "ExampleSite"
    titles = ["First Article", "Second Article", "Third Article"]
    show_list(site, titles)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().splitlines()
    assert output_lines[0] == f"The latest tutorials from {site}"
    for idx, title in enumerate(titles):
        assert output_lines[idx + 1] == f"{idx:>3} {title}"

def test_show_list_empty_titles(capsys):
    site = "EmptySite"
    titles = []
    show_list(site, titles)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().splitlines()
    assert output_lines == [f"The latest tutorials from {site}"]