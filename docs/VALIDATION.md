# Validation — website 2.3.1

Prepared 26 September 2026 UTC. Contact-only website update: **comercial@mywavelink.com**. These checks concern the supplied static website, not email delivery, Wavelink application readiness or a customer deployment.

## Source integrity and exact scope

Input ZIP: `Wavelink_Website_2.3.0_GitHub.zip`.
SHA-256: `2fa0f07be43c3b60f310bf3843d7385932bbd5530ff7e90e8f30710ca540afba`.
All 32 parent file-manifest entries were verified for size and SHA-256. An exact byte comparison of the published `site` directory confirms the only changes are the contact address and the website release/cache version. All images, section content, module coverage, demo destinations, CSS rules and JavaScript behaviour are preserved. The final manifest lists delivered files excluding itself and compares them to that verified parent.

## Passed

**Static/contact checks:** `python tools/check_site.py --json docs/static-checks.json`.
All eight mailto links, the copy-email value, displayed addresses and repository text use **comercial@mywavelink.com**. No other address remains in repository text. Original email subjects are preserved. Checks also cover HTML metadata, headings, duplicate IDs, local links and anchors, ARIA references, image attributes, expected domains, separate demo links, seven panel targets, planned-security labels, no unexpected form/login/storage/API code, reduced motion, sitemap and total asset payload. This is not a complete HTML conformance or accessibility audit.

**JavaScript syntax:** `node --check site/script.js`.

**Chromium rendering and interactions:**
`python tools/browser_smoke.py --in-memory --browser /usr/bin/chromium --out <review folder>`.
Chromium 144.0.7559.96. Ten viewport widths: 320, 390, 600, 768, 959, 960, 1024, 1280, 1440 and 1920 pixels. Exact local HTML/CSS/images are embedded without external requests and the shipped JS is injected after parsing.

Checks include six permanent capability cards; full-platform headline; Overview as sole default selection; all seven panels; overview links selecting/focusing their matching views; keyboard activation and wrapping; fourteen capability entries; eight FAQ disclosures; mobile navigation and focus handling; planned-security labels; no credential fields; reduced motion; no horizontal overflow in tested states; no runtime errors.

Additional cases passed: JavaScript-disabled mobile fallback, clipboard success/failure handlers with deterministic stubs, mobile privacy page and mobile 404 page. The clipboard success test verifies the exact new address; the stubs do not test operating-system clipboard permissions.

**Targeted contact review:** email destinations and copy-email value verified at 320, 390 and 1440 pixels. Contact-section screenshots checked at desktop and mobile sizes, with no horizontal overflow. Privacy links checked at 390 pixels. These are website previews, not app screenshots.

**Local HTTP byte comparison:** `python tools/check_http.py --json docs/http-checks.json`.
A Python loopback server returned every published file byte-for-byte. No external host was contacted.

## Browser HTTP and deployment limits

This release's browser checks use in-memory rendering, not browser HTTP navigation. `browser-http-attempt.json` is retained historical evidence from parent 2.3.0, whose normal Playwright loopback navigation was blocked by the environment (`net::ERR_BLOCKED_BY_ADMINISTRATOR`). It is not a new test or pass for 2.3.1. The separate Python loopback-byte test was rerun successfully for 2.3.1. Browser HTTP navigation needs review after upload or in an unrestricted local environment.

No GitHub push, Render deployment, DNS update, public website/demo availability check, mailbox configuration, email delivery, domain redirect, live 404 hosting test, physical phone test, Safari/Firefox test, formal WCAG audit, external security audit or application authentication/permissions test was performed. Public social-card caching was not tested.

Use [../UPDATE_GITHUB.md](../UPDATE_GITHUB.md) after deployment. No test here establishes that the live website already matches these files. Having a company contact email does not implement company-email sign-in or two-step verification in the application.
