"""Static acceptance checks for the English marketing workflow pages; no network."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'site'
BASE = 'https://www.mywavelink.com/'
GUIDES = ('offshore-equipment-inventory.html', 'offshore-cargo-manifests.html',
          'offshore-shift-handovers.html', 'offshore-crew-rotation-software.html')


class Document(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.tags = []
        self.feed((ROOT / filename).read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def find(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and attrs.items() <= a.items()]


def main():
    home = Document('index.html')
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('{*}url/{*}loc')]
    assert len(set(urls)) == len(urls), 'Sitemap contains duplicate URLs'
    assert BASE in urls and all(url.startswith(BASE) for url in urls), 'Unexpected sitemap host'
    assert all((ROOT / (urlparse(url).path.lstrip('/') or 'index.html')).is_file() for url in urls)
    for filename in (*GUIDES, 'privacy.html'):
        doc = Document(filename)
        canonical = BASE + filename
        # Disk previews ignore the web-only base. Hosted pages use it within their own origin.
        policies = {attrs.get('content') for attrs in doc.find('meta', **{'http-equiv': 'Content-Security-Policy'})}
        assert {"base-uri 'self'", 'base-uri http: https:'} <= policies, filename
        for path in (filename, Path(filename).stem, Path(filename).stem + '/'):
            page_url = BASE + path
            bases = doc.find('base')
            page_base = urljoin(page_url, bases[0]['href']) if bases else page_url
            for tag, attrs in doc.tags:
                for field in ('href', 'src'):
                    target = attrs.get(field)
                    if tag != 'base' and target:
                        assert urljoin(page_base, target) == urljoin(canonical, target), (
                            f'{path}: {target} resolves to a different destination'
                        )
    seen_titles, seen_descriptions = set(), set()
    for filename in ('index.html', *GUIDES):
        doc = Document(filename)
        canonical = BASE + (filename if filename != 'index.html' else '')
        assert canonical in urls
        assert doc.find('link', rel='canonical') == doc.find('link', rel='canonical', href=canonical)
        assert len(doc.find('link', rel='canonical')) == 1
        for tag in ('h1', 'title', 'main'):
            assert len(doc.find(tag)) == 1
        assert doc.find('html', lang='en')
        assert doc.find('a', href='#main') and doc.find('main', id='main')
        assert not any('noindex' in t.get('content', '').lower() for t in doc.find('meta', name='robots'))
        title = doc.find('meta', property='og:title')[0]['content']
        desc = doc.find('meta', name='description')[0]['content']
        assert desc and title and title not in seen_titles and desc not in seen_descriptions
        seen_titles.add(title)
        seen_descriptions.add(desc)
        if filename in GUIDES:
            assert len(home.find('a', href=filename)) >= 2, 'Missing homepage links: ' + filename
            assert any(doc.find('a', href=x) for x in GUIDES if x != filename)
            assert len(doc.find('h2')) >= 3
            assert doc.find('nav', **{'aria-label':'Main navigation'})
            assert doc.find('a', href='https://demo.mywavelink.com/__demo/public')
    print(f'Passed: {len(GUIDES)} workflow guides, {len(urls)} public sitemap URLs, unique metadata and crawlable links.')


if __name__ == '__main__':
    main()
