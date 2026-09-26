# Validation — website 2.3.0

Prepared 26 September 2026 UTC. These checks concern the supplied static website, not Wavelink application readiness or a customer deployment.

## Source integrity

Input ZIP: `Wavelink_Website_2.2.0_GitHub.zip`.
SHA-256: `99fc207ff82a14fef7978f273667cb353a9052b9faba24354c1d39e23c3c2d1c`.
All 31 parent file-manifest entries were verified for size and SHA-256 before editing. The final manifest lists the delivered files excluding itself, with comparison to the parent.

## Passed

**Static checks:** `python tools/check_site.py --json docs/static-checks.json`.
Checks HTML metadata, one h1 per page, duplicate IDs, local links and anchors, ARIA references, image attributes, expected domains, separate demo links, seven panel targets, planned-security labels, absence of old workflow widgets and external script/image dependencies, no form/login/storage/API code, reduced-motion support, sitemap and total asset payload. This is not a complete HTML conformance or accessibility audit.

**JavaScript syntax:** `node --check site/script.js`.

**Chromium rendering and interactions:**
`python tools/browser_smoke.py --in-memory --browser /usr/bin/chromium --out <review folder>`.
Chromium 144.0.7559.96. Ten viewport widths: 320, 390, 600, 768, 959, 960, 1024, 1280, 1440 and 1920 pixels. The shipped HTML/CSS/images are embedded without external requests and the exact shipped JS is injected after parsing.

Checks include six permanent capability cards; whole-platform headline; Overview as the sole default selection; all seven panels; each of six overview links selecting/focusing its matching view; manual keyboard activation and wrapping; fourteen capability entries; eight FAQ disclosures; mobile navigation, Escape, outside-click and focus handling; explicit planned-security labels; no credential fields; reduced motion; no horizontal overflow in all tested states; no runtime errors.

Additional cases: JavaScript-disabled mobile fallback, clipboard success/failure code paths with deterministic stubs, mobile privacy page, mobile 404 page. The stubs do not test operating-system clipboard permissions.

**Local HTTP byte comparison:** `python tools/check_http.py --json docs/http-checks.json`.
A Python loopback server returned each published file byte-for-byte. No external host was contacted.

**Visual review:** desktop and mobile hero screenshots, full-page layout and the full-platform/product overview sections were inspected. Screenshots are previews of the website, not screenshots of the Wavelink app.

## Browser HTTP test was blocked

The normal Playwright `page.goto` test against the temporary loopback server returned `net::ERR_BLOCKED_BY_ADMINISTRATOR` before rendering. This environment restriction is recorded in `browser-http-attempt.json`; it is not presented as a pass or a website defect. In-memory checks and the separate Python HTTP-byte test are the completed alternatives. Actual browser HTTP navigation still needs review after upload or in an unrestricted local environment.

## Not tested / not performed

No GitHub push, Render deployment, DNS update, public website/demo availability check, email delivery, domain redirect, live 404 hosting behaviour, physical phone test, Safari/Firefox test, formal WCAG audit, external security audit or application authentication/permissions test. Public social-card caching was not tested.

Use [../UPDATE_GITHUB.md](../UPDATE_GITHUB.md) for the checks to make after deployment. No test result here establishes that the live website already matches these files.
