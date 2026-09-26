#!/usr/bin/env python3
"""Optional Chromium smoke checks (requires the Python playwright package).

Normal local HTTP test:
  python tools/browser_smoke.py
Restricted rendering environment, no navigation requests:
  python tools/browser_smoke.py --in-memory --browser /path/to/chromium

--in-memory embeds the exact local CSS/images and injects the shipped JS after
parsing, equivalent to its defer timing. Link destinations are validated by
check_site.py; in-memory mode does NOT test HTTP navigation or deployment.
"""
from __future__ import annotations

import argparse
import base64
import functools
import http.server
import json
import mimetypes
import re
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'


def embedded_html(filename: str) -> str:
    html = (SITE / filename).read_text(encoding='utf-8')
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.S)

    def link(match: re.Match) -> str:
        tag = match.group(0)
        if 'rel="stylesheet"' in tag:
            return '<style>' + (SITE / 'styles.css').read_text(encoding='utf-8') + '</style>'
        if any(value in tag for value in ['rel="icon"', 'rel="alternate icon"', 'rel="apple-touch-icon"']):
            return ''
        return tag
    html = re.sub(r'<link\b[^>]*>', link, html)

    def asset(match: re.Match) -> str:
        path = SITE / match.group(2).lstrip('/')
        if not path.is_file():
            return match.group(0)
        mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        data = base64.b64encode(path.read_bytes()).decode('ascii')
        return match.group(1) + 'data:' + mime + ';base64,' + data + match.group(3)
    return re.sub(r'((?:src|srcset)=")([^"]+)(")', asset, html)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--in-memory', action='store_true')
    ap.add_argument('--browser', type=str, help='Optional Chromium executable path')
    ap.add_argument('--out', type=Path, default=ROOT / 'test-output')
    args = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit('Optional tests require playwright. Install it in your development environment, not in the website deployment.')
    args.out.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    errors: list[str] = []
    server = None
    base_url = ''
    if not args.in_memory:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base_url = f'http://127.0.0.1:{server.server_port}/'

    def load(page, name='index.html', js=True):
        if args.in_memory:
            page.set_content(embedded_html(name), wait_until='load')
            if js:
                page.add_script_tag(content=(SITE / 'script.js').read_text(encoding='utf-8'))
                # Local anchor/default behaviour cannot navigate under the restricted
                # browser policy. Production handlers still receive every click.
                page.evaluate("document.addEventListener('click', e => { if (e.target.closest('a')) e.preventDefault(); })")
        else:
            page.goto(base_url + name, wait_until='networkidle')
        page.emulate_media(reduced_motion='reduce')

    def no_overflow(page):
        bad = page.evaluate('''() => [...document.querySelectorAll('body *')].filter(e => {
            const r = e.getBoundingClientRect();
            return r.width > 0 && (r.right > innerWidth + 1 || r.left < -1)
                && !e.classList.contains('sr-only') && !e.classList.contains('skip-link');
        }).map(e => `${e.tagName}.${typeof e.className === 'string' ? e.className : 'svg'}`);''')
        assert not bad, f'Horizontal overflow: {bad[:10]}'

    try:
        with sync_playwright() as p:
            launch = {'headless': True, 'args': ['--no-sandbox']}
            if args.browser:
                launch['executable_path'] = args.browser
            browser = p.chromium.launch(**launch)
            version = browser.version
            for width in [320, 390, 600, 768, 959, 960, 1024, 1280, 1440, 1920]:
                context = browser.new_context(viewport={'width': width, 'height': 950}, device_scale_factor=1)
                page = context.new_page()
                page.set_default_timeout(7000)
                runtime_errors: list[str] = []
                page.on('pageerror', lambda error: runtime_errors.append(str(error)))
                load(page)
                no_overflow(page)
                assert page.locator('h1').count() == 1
                assert page.locator('[role="tab"][aria-selected="true"]').count() == 1
                assert page.locator('#panel-overview').is_visible()
                assert page.locator('#inventory').is_visible()
                assert page.locator('#manifests').is_visible()
                assert 'Your whole' in page.locator('h1').inner_text()
                assert 'Working as one.' in page.locator('h1').inner_text()
                assert page.locator('.scope-grid > article:visible').count() == 6
                assert page.locator('.operation-domain:visible').count() == 6
                assert page.locator('#inventory').bounding_box()['y'] < page.locator('#platform').bounding_box()['y']
                assert page.locator('#manifests').bounding_box()['y'] < page.locator('#platform').bounding_box()['y']
                for key in ['inventory', 'manifests', 'readiness', 'handovers', 'checks', 'logs']:
                    page.locator(f'.scope-grid [data-preview="{key}"]').click()
                    assert page.locator(f'#panel-{key}').is_visible()
                    assert page.locator(f'#tab-{key}').evaluate('e => e === document.activeElement')
                    no_overflow(page)
                heights = {}
                keys = ['overview', 'inventory', 'manifests', 'handovers', 'checks', 'readiness', 'logs']
                for key in keys:
                    page.locator(f'#tab-{key}').click()
                    assert page.locator(f'#panel-{key}').is_visible()
                    assert page.locator(f'#tab-{key}').get_attribute('aria-selected') == 'true'
                    assert page.locator('[role="tabpanel"]:visible').count() == 1
                    heights[key] = page.locator(f'#panel-{key} .workspace-window').bounding_box()['height']
                    no_overflow(page)
                page.locator('#tab-overview').click()
                page.locator('#tab-overview').press('End')
                assert page.locator('#tab-logs').evaluate('e => e === document.activeElement')
                assert page.locator('#tab-overview').get_attribute('aria-selected') == 'true'
                page.locator('#tab-logs').press('Enter')
                assert page.locator('#panel-logs').is_visible()
                page.locator('#tab-logs').press('Home')
                page.locator('#tab-overview').press('Space')
                assert page.locator('#panel-overview').is_visible()
                page.locator('#tab-overview').press('ArrowLeft')
                assert page.locator('#tab-logs').evaluate('e => e === document.activeElement')
                page.locator('#tab-logs').press('ArrowRight')
                assert page.locator('#tab-overview').evaluate('e => e === document.activeElement')
                directory = page.locator('.capability-directory')
                directory.locator('summary').click()
                assert directory.get_attribute('open') is not None
                assert directory.locator('.capability-grid article:visible').count() == 14
                no_overflow(page)
                directory.locator('summary').click()
                assert directory.get_attribute('open') is None
                for i in range(page.locator('.faq-item').count()):
                    faq = page.locator('.faq-item').nth(i)
                    faq.locator('summary').click()
                    assert faq.get_attribute('open') is not None
                    no_overflow(page)
                    faq.locator('summary').click()
                    assert faq.get_attribute('open') is None
                assert page.locator('.security-card.is-planned').count() == 2
                for card in page.locator('.security-card.is-planned').all():
                    assert 'PLANNED' in card.locator('.security-state').inner_text()
                    assert 'Future release' in card.inner_text()
                assert page.locator('input, form, iframe').count() == 0
                if width < 960:
                    button = page.locator('.menu-toggle')
                    assert button.is_visible()
                    button.click()
                    assert button.get_attribute('aria-expanded') == 'true'
                    button.press('Escape')
                    assert button.get_attribute('aria-expanded') == 'false'
                    assert button.evaluate('e => e === document.activeElement')
                    button.click()
                    page.locator('#site-nav a[href="#security"]').click()
                    assert button.get_attribute('aria-expanded') == 'false'
                    assert page.locator('#security').evaluate('e => e === document.activeElement')
                    button.click()
                    page.mouse.click(width - 6, 920)
                    assert button.get_attribute('aria-expanded') == 'false'
                else:
                    assert page.locator('.menu-toggle').is_hidden()
                    assert page.locator('#site-nav').is_visible()
                assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == 'auto'
                assert not runtime_errors, runtime_errors
                page.evaluate('document.activeElement.blur(); window.scrollTo(0, 0)')
                if width in [390, 1440]:
                    page.screenshot(path=str(args.out / f'website-{width}-full.png'), full_page=True)
                    page.screenshot(path=str(args.out / f'website-{width}-hero.png'))
                results.append({'viewport_width': width, 'passed': True, 'product_window_heights': heights,
                                'checks': ['six permanent capability areas, including Inventory and Manifests, before the product tabs', 'all six overview links select and focus the matching product view', '7 panels with platform Overview default, separate Inventory and Manifests', 'no horizontal overflow in every panel, expanded directory and each FAQ', '14-capability disclosure', 'manual keyboard focus/activation with wraparound', 'all 8 FAQs', 'mobile/desktop navigation', 'explicit planned-security labels', 'no credential fields or embedded application', 'reduced motion', 'no JavaScript runtime errors']})
                context.close()

            context = browser.new_context(viewport={'width': 390, 'height': 844}, java_script_enabled=False)
            page = context.new_page()
            load(page, js=False)
            assert page.locator('#site-nav').is_visible()
            assert page.locator('.module-tabs').is_hidden()
            assert page.locator('#panel-overview').is_visible()
            assert page.locator('#inventory').is_visible()
            assert page.locator('#manifests').is_visible()
            page.locator('.capability-directory summary').click()
            assert page.locator('.capability-grid article:visible').count() == 14
            page.locator('.faq-item summary').first.click()
            assert page.locator('.faq-item').first.get_attribute('open') is not None
            no_overflow(page)
            results.append({'test': 'JavaScript-disabled mobile', 'passed': True,
                            'checks': ['navigation available', 'overview preview and all six permanent capability areas available', 'all 14 capabilities accessible through native disclosure', 'native FAQ works', 'no overflow']})
            context.close()

            context = browser.new_context(viewport={'width': 390, 'height': 844})
            page = context.new_page()
            load(page)
            # Deterministic API stubs exercise both permission outcomes, not the OS clipboard.
            page.evaluate("Object.defineProperty(window, 'isSecureContext', {value:true, configurable:true}); Object.defineProperty(navigator, 'clipboard', {value:{writeText:async text=>{window.__copied=text;}}, configurable:true});")
            page.locator('[data-copy-email]').click()
            assert page.locator('#copy-status').inner_text() == 'Email address copied.'
            assert page.evaluate('window.__copied') == 'adriano5454@gmail.com'
            page.evaluate("Object.defineProperty(navigator, 'clipboard', {value:{writeText:async()=>{throw new Error('Denied');}}, configurable:true});")
            page.locator('[data-copy-email]').click()
            assert 'select and copy' in page.locator('#copy-status').inner_text()
            results.append({'test': 'Clipboard success/failure handlers with stubs', 'passed': True})
            for name in ['privacy.html', '404.html']:
                load(page, name)
                no_overflow(page)
                assert page.locator('h1').is_visible()
                results.append({'test': f'{name} mobile rendering', 'passed': True})
            context.close()
            browser.close()
    except Exception as exc:
        errors.append(f'{type(exc).__name__}: {exc}')
        version = locals().get('version', 'not started')
    finally:
        if server:
            server.shutdown()
            server.server_close()
    report = {'release': 'website-2.3.0', 'passed': not errors, 'browser': f'Chromium {version}',
              'mode': 'in-memory local assets, shipped JS injected after DOM parse' if args.in_memory else 'local HTTP',
              'results': results, 'errors': errors,
              'not_tested': ['live GitHub/Render deployment', 'public website or demo availability', 'physical mobile devices', 'Safari and Firefox', 'native OS clipboard permissions', 'formal WCAG conformance']}
    (args.out / 'browser-checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
