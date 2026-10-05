# Website 3.1.0 validation

Executed on the release source. This verifies the website; it does not retest the Wavelink application or certify a production deployment.

- Attached website baseline: all **33 Git blobs** match website main `ea8ec477d6c4f699e09d34b293c315a2f1a5b5d8`.
- Content: current UI95 application docs plus the retained feature/security releases were read at `dd8eff975a594e41b10bf5e589577bcf4e954cee`.
- Static checks: three pages, one H1 each, unique IDs, local assets, page/anchor destinations, protected new-tab links, current contact/demo destinations, JSON-LD and content limits passed.
- JavaScript syntax: `node --check site/script.js` passed.
- Local HTTP: all **14** published files returned 200 and matched source bytes exactly.
- Browser: Chromium **153.0.8010.12**; **18 widths** (320, 390, 600, 740, 741, 768, 900, 1000, 1001, 1024, 1100, 1101, 1150, 1151, 1200, 1280, 1440, 1920).
- All seven explorer categories, one visible panel, keyboard Home/End/arrows/activation, all 18 directory links/counts, Imports cross-link, mobile menu and Escape, all eight FAQs, clipboard success/denial, privacy/404 layout and deep links passed. Four planned labels, three keyboard-operated package disclosures, the package navigation anchor and HR enquiry destination were checked.
- No horizontal overflow or unexpected JavaScript error in the reviewed states. The enlarged-text check at 1280 pixels and no-JavaScript check at 390 pixels passed.
- The package section was visually inspected at desktop and phone widths with its additional scope expanded. Enlarged text and no-JavaScript interaction were checked. The earlier header and full-platform visual review is retained as a baseline. Supplied offshore imagery and the existing social image are unchanged.

Browser requests were fulfilled from local source at a synthetic HTTPS origin. Python HTTP checks used a real temporary loopback server. These are separate scopes; this is not external DNS, live hosting, public-demo login, inbox delivery, physical-device or application-runtime acceptance.

Initial browser harness runs exposed a single-process Chromium context limitation. The current harness reuses one context and disables script execution through CDP for its no-JavaScript check. The final corrected run passes; earlier harness failures are not represented as website passes.

During the earlier 3.0.0 delivery, GitHub read access succeeded for both repositories. Branch creation returned **403 — Resource not accessible by integration**. No remote branch, commit, pull request or hosting deployment was created. The complete release package is available for the usual website checkout/commit/push workflow.

The filled navy demo action, separate contact action and hover/focus states are retained. Header navigation now includes HR packages. Compact navigation starts at 1150 pixels, keeping the additional package link out of a crowded desktop row. The earlier 3.0.1 header report remains a historical check of contact anchors, menu resize and a protected demo tab using a local demo stub; it is not a new 3.1.0 live-demo test.

Planned package copy was reviewed separately for availability clarity and offshore relevance. These are proposed future requirements from the user, not an application release audit. The website adds no HR data collection or runtime workflows.

The targeted layout check found a wrapped desktop header after the new navigation link was added. The final CSS uses a compact menu through 1150 pixels and tighter desktop navigation up to 1280 pixels. The corrected run verifies a single header row at normal text size above 1150 pixels.

Structured reports: `static-checks.json`, `http-checks.json`, `browser-checks.json`, `header-checks.json`, `package-layout-checks.json`. Bulky screenshots remain outside the deployment source package.
