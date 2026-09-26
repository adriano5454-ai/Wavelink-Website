#!/usr/bin/env python3
"""Check this static website without third-party packages or network access.

Run from any directory: python tools/check_site.py
Optional JSON report: python tools/check_site.py --json docs/static-checks.json
This is a structural smoke check, not a complete accessibility/security audit.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
DEMO = 'https://demo.mywavelink.com/'
PUBLIC = 'https://www.mywavelink.com'
CONTACT_EMAIL = 'comercial@mywavelink.com'


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str | None], int]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs), self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json', type=Path, help='Write a machine-readable report.')
    args = ap.parse_args()
    errors: list[str] = []
    checks: list[str] = []
    documents: dict[Path, PageParser] = {}
    for path in sorted(SITE.glob('*.html')):
        parser = PageParser()
        parser.feed(path.read_text(encoding='utf-8'))
        documents[path.resolve()] = parser
    if not documents:
        errors.append('No HTML files found under site/.')

    for path, doc in documents.items():
        label = path.name
        ids = [a['id'] for _, a, _ in doc.tags if a.get('id')]
        duplicates = [key for key, count in Counter(ids).items() if count > 1]
        if duplicates:
            errors.append(f'{label}: duplicate IDs {duplicates}')
        if sum(t == 'h1' for t, _, _ in doc.tags) != 1:
            errors.append(f'{label}: expected exactly one h1.')
        if not any(t == 'html' and a.get('lang') == 'en' for t, a, _ in doc.tags):
            errors.append(f'{label}: missing English language declaration.')
        if not any(t == 'meta' and a.get('name') == 'viewport' for t, a, _ in doc.tags):
            errors.append(f'{label}: missing viewport metadata.')
        if not any(t == 'title' for t, _, _ in doc.tags):
            errors.append(f'{label}: missing title.')
        if not any(t == 'meta' and a.get('name') == 'description' for t, a, _ in doc.tags):
            errors.append(f'{label}: missing description.')

        for tag, attrs, line in doc.tags:
            where = f'{label}:{line}'
            if tag == 'img' and 'alt' not in attrs:
                errors.append(f'{where}: image is missing alt attribute.')
            if tag == 'img' and not (attrs.get('width') and attrs.get('height')):
                errors.append(f'{where}: image needs intrinsic width and height.')
            if tag == 'a' and attrs.get('target') == '_blank':
                if 'noopener' not in (attrs.get('rel') or '').split():
                    errors.append(f'{where}: new-tab link lacks noopener.')
            if tag == 'a' and attrs.get('href', '').startswith('https://demo.'):
                if attrs['href'] != DEMO:
                    errors.append(f'{where}: unexpected demo URL {attrs["href"]}.')
            if tag in {'form', 'iframe'}:
                errors.append(f'{where}: unexpected form or iframe; review data-handling copy.')
            if tag == 'button' and attrs.get('type') != 'button':
                errors.append(f'{where}: button needs explicit type="button".')
            for aria in ['aria-controls', 'aria-labelledby']:
                for item in (attrs.get(aria) or '').split():
                    if item not in ids:
                        errors.append(f'{where}: {aria} points to missing ID {item}.')
            for attr in ['href', 'src', 'srcset']:
                value = attrs.get(attr)
                if not value:
                    continue
                # The source srcset intentionally contains one local image, no descriptors.
                if attr == 'srcset':
                    value = value.split(',')[0].strip().split()[0]
                parts = urlsplit(value)
                if parts.scheme or parts.netloc:
                    if tag in {'script', 'img', 'source', 'iframe'} and parts.scheme != 'data':
                        errors.append(f'{where}: unexpected external asset {value}.')
                    continue
                raw_path = unquote(parts.path)
                target = (SITE / raw_path.lstrip('/') if raw_path.startswith('/') else path.parent / raw_path).resolve() if raw_path else path
                if target.is_dir():
                    target = target / 'index.html'
                if not target.is_relative_to(SITE.resolve()) or not target.is_file():
                    errors.append(f'{where}: missing or out-of-site {attr} target {value}.')
                    continue
                if parts.fragment and target.suffix == '.html':
                    other = documents.get(target)
                    if other and not any(a.get('id') == unquote(parts.fragment) for _, a, _ in other.tags):
                        errors.append(f'{where}: broken anchor {value}.')
        checks.append(f'{label}: headings, language, metadata, IDs, links, assets, controls and image attributes checked')

    email_links = 0
    copy_values = 0
    for path, doc in documents.items():
        for tag, attrs, line in doc.tags:
            href = attrs.get('href') or ''
            if href.lower().startswith('mailto:'):
                email_links += 1
                recipient = unquote(urlsplit(href).path)
                if recipient != CONTACT_EMAIL:
                    errors.append(f'{path.name}:{line}: unexpected contact recipient {recipient}.')
            if 'data-copy-email' in attrs:
                copy_values += 1
                if attrs['data-copy-email'] != CONTACT_EMAIL:
                    errors.append(f'{path.name}:{line}: copy-email target is incorrect.')
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        for address in re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text):
            if address != CONTACT_EMAIL:
                errors.append(f'{path.relative_to(ROOT)}: unexpected email address {address}.')
    if email_links < 1 or copy_values != 1:
        errors.append(f'Expected contact links and one copy-email control; found {email_links} / {copy_values}.')
    checks.append(f'Contact: {email_links} mailto links and {copy_values} copy-email value use {CONTACT_EMAIL}; repository text checked for other addresses')

    home = (SITE / 'index.html').read_text(encoding='utf-8')
    if f'href="{PUBLIC}/"' not in home:
        errors.append('Canonical home URL is not the expected public website.')
    for required in ['panel-overview', 'overview', 'maintenance', 'continuity', 'safety', 'fleet', 'panel-inventory', 'panel-manifests', 'panel-handovers', 'panel-checks', 'panel-readiness', 'panel-logs', 'inventory', 'manifests', 'teams', 'security', 'deployment']:
        if f'id="{required}"' not in home:
            errors.append(f'Missing expected illustrative view: {required}')
    for phrase in ['PLANNED PROTECTION', 'PLANNED COMPANY ACCESS', 'Future release · Planned', 'Two-step verification', 'Your company email', 'not security guarantees for the public demo']:
        if phrase not in home:
            errors.append(f'Missing required security-status wording: {phrase}')
    if 'EXPLORE THE WORKFLOWS' in home or 'stage-receive' in home:
        errors.append('Obsolete workflow widget or asset journey remains.')
    if any(tag in home for tag in ['<input', '<form', '<iframe']):
        errors.append('Unexpected data collection/login interface in marketing site.')
    for phrase in ['THE CONNECTED OFFSHORE OPERATIONS PLATFORM', 'Your whole', 'Working as one.', 'Fault reports', 'HSE / QSHE', 'Handovers &amp; tasks', 'STOCK / STATUS', 'SHIPMENT CONTENTS', 'QR verification', 'Low-stock alerts', 'Awaiting placement', 'Receipt confirmed', 'data-preview="inventory"', 'data-preview="manifests"']:
        if phrase not in home:
            errors.append(f'Missing required inventory/manifest messaging: {phrase}')
    home_doc = documents[SITE / 'index.html']
    selected = [a.get('id') for tag, a, _ in home_doc.tags if a.get('role') == 'tab' and a.get('aria-selected') == 'true']
    if selected != ['tab-overview']:
        errors.append(f'Overview is not the only default selected preview: {selected}')
    checks.append('Whole-platform messaging, overview default, permanent inventory/manifests and six-area breadth, collaboration and planned-security labels checked')
    js = (SITE / 'script.js').read_text(encoding='utf-8')
    for pattern in [r'\bfetch\s*\(', r'\bXMLHttpRequest\b', r'\blocalStorage\b', r'\bsessionStorage\b', r'\bdocument\.cookie\b']:
        if re.search(pattern, js):
            errors.append(f'Unexpected network/storage pattern {pattern}; review privacy information.')
    css = (SITE / 'styles.css').read_text(encoding='utf-8')
    if '@font-face' in css or re.search(r'@import\b', css):
        errors.append('Unexpected external/bundled-font or imported CSS dependency.')
    if 'prefers-reduced-motion' not in css:
        errors.append('Reduced-motion preference support missing.')
    checks.append('Demo URL, illustration targets, reduced motion, and no network/storage code checked')

    try:
        tree = ElementTree.parse(SITE / 'sitemap.xml')
        for loc in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            url = (loc.text or '').strip()
            if not url.startswith(PUBLIC + '/'):
                errors.append(f'Unexpected sitemap URL {url}')
                continue
            relative = url.removeprefix(PUBLIC + '/') or 'index.html'
            if not (SITE / relative).is_file():
                errors.append(f'Sitemap target missing: {url}')
    except (OSError, ElementTree.ParseError) as exc:
        errors.append(f'Sitemap error: {exc}')
    if PUBLIC + '/sitemap.xml' not in (SITE / 'robots.txt').read_text(encoding='utf-8'):
        errors.append('robots.txt has no expected sitemap URL.')
    if not (SITE / 'assets/wavelink-social.jpg').is_file():
        errors.append('Social share image missing.')
    checks.append('Sitemap, robots file and social-share asset checked')
    site_bytes = sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())
    if site_bytes > 1_000_000:
        errors.append(f'Site assets exceed the 1 MB review budget: {site_bytes:,} bytes.')
    checks.append(f'Total published site payload: {site_bytes:,} bytes (all files, not a single page load)')
    report = {'release': 'website-2.3.1', 'passed': not errors, 'checks': checks, 'errors': errors, 'site_bytes': site_bytes, 'network_requests_made': False}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    for check in checks:
        print(f'CHECK  {check}')
    for error in errors:
        print(f'ERROR  {error}', file=sys.stderr)
    print('PASS' if not errors else f'FAIL: {len(errors)} issue(s)')
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
