import pytest
from unittest.mock import patch
from scrape import get_links_from_page, get_all_links, save_counts_to_csv
import csv
import os

# Sample HTML snippet for get_links_from_page test
SAMPLE_HTML = """
<html><body>
  <div class="mw-category mw-category-columns">
    <a href="/wiki/Animal1">Animal1</a>
    <a href="/wiki/Animal2">Animal2</a>
  </div>
  <div class="mw-category-generated">
    <a href="/wiki/Next_Page">Следующая страница</a>
  </div>
</body></html>
"""

class FakeResponse:
    def __init__(self, text):
        self.text = text
    def raise_for_status(self):
        pass

@pytest.fixture
def fake_requests_get():
    with patch('scrape.requests.get') as mock_get:
        mock_get.return_value = FakeResponse(SAMPLE_HTML)
        yield mock_get

def test_get_links_from_page(fake_requests_get):
    links, next_url = get_links_from_page("https://fake-url.com")
    assert links == ["/wiki/Animal1", "/wiki/Animal2"]
    assert next_url is not None
    assert "Next_Page" in next_url

def test_get_all_links(fake_requests_get):
    # It will loop infinitely because mocked next page is always the same
    # So we patch get_links_from_page to limit pages
    from scrape import get_links_from_page as real_get_links

    call_count = {'count': 0}
    def limited_get_links(url):
        call_count['count'] += 1
        if call_count['count'] > 3:
            return [], None
        return real_get_links(url)

    with patch('scrape.get_links_from_page', side_effect=limited_get_links):
        counts = get_all_links("https://fake-url.com")
        # Animal1 and Animal2 start with 'A'
        assert counts.get('A', 0) == 6  # 2 links per page * 3 pages
        assert sum(counts.values()) == 6

def test_save_counts_to_csv(tmp_path):
    counts = {'A': 2, 'B': 5}
    file = tmp_path / "counts.csv"
    save_counts_to_csv(counts, file)

    with open(file, encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ['Letter', 'Count']
    assert ['A', '2'] in rows
    assert ['B', '5'] in rows
