# Website 3.0.1 validation

Executed on the release source. This verifies the website; it does not retest the Wavelink application or certify a production deployment.

- Attached website baseline: all **33 Git blobs** match website main `ea8ec477d6c4f699e09d34b293c315a2f1a5b5d8`.
- Content: current UI95 application docs plus the retained feature/security releases were read at `dd8eff975a594e41b10bf5e589577bcf4e954cee`.
- Static checks: three pages, one H1 each, unique IDs, local assets, page/anchor destinations, protected new-tab links, current contact/demo destinations, JSON-LD and content limits passed.
- JavaScript syntax: `node --check site/script.js` passed.
- Local HTTP: all **14** published files returned 200 and matched source bytes exactly.
- Browser: Chromium **153.0.8010.12**; **13 widths** (320, 390, 600, 740, 741, 768, 900, 1000, 1001, 1024, 1280, 1440, 1920).
- All seven explorer categories, one visible panel, keyboard Home/End/arrows/activation, all 18 directory links/counts, Imports cross-link, mobile menu and Escape, all seven FAQs, clipboard success/denial, privacy/404 layout and deep links passed.
- No horizontal overflow or unexpected JavaScript error in the reviewed states. The enlarged-text check at 1280 pixels and no-JavaScript check at 390 pixels passed.
- Desktop header, hover styling, mobile menu and enlarged-text header renders were visually inspected. The prior full-page and panel review is retained as the content/layout baseline. Supplied offshore imagery and the existing social image are unchanged.

Browser requests were fulfilled from local source at a synthetic HTTPS origin. Python HTTP checks used a real temporary loopback server. These are separate scopes; this is not external DNS, live hosting, public-demo login, inbox delivery, physical-device or application-runtime acceptance.

Initial browser harness runs exposed a single-process Chromium context limitation. The current harness reuses one context and disables script execution through CDP for its no-JavaScript check. The final corrected run passes; earlier harness failures are not represented as website passes.

During the earlier 3.0.0 delivery, GitHub read access succeeded for both repositories. Branch creation returned **403 — Resource not accessible by integration**. No remote branch, commit, pull request or hosting deployment was created. The complete release package is available for the usual website checkout/commit/push workflow.

Header refinement: filled navy demo action with teal arrow, separate contact action, larger link targets and hover/focus states. Compact navigation starts at 1000 pixels. Contact anchors, menu resize and a new-tab/no-opener demo link were checked with local-source requests and a local demo stub; the live demo was not contacted.

Structured reports: `static-checks.json`, `http-checks.json`, `browser-checks.json`, `header-checks.json`. Bulky screenshots remain outside the deployment source package.
