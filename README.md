# Wavelink website 3.0.1

A complete refresh of the Wavelink marketing website, checked against application **UI95**. Equipment and logistics, daily work, safety, people and company control now share a clear product story.

The offshore opening leads to seven interactive product categories and an expandable directory of 18 capability areas. Dedicated sections explain document/worksheet imports, the shore-to-vessel workflow, profiles and contribution badges, personal actions, optional email alerts, company membership, two-step verification and hosted/local deployment.

The 3.0.1 refinement strengthens the header navigation with clearer hover/focus states, a separate contact action and a filled demo button. The compact menu now starts at 1000 pixels so tablet navigation has room. The rest of the page and its feature copy remain unchanged.

## Review or publish

This is the **full clean replacement repository**. Follow [RESTORE_FULL_WEBSITE.md](RESTORE_FULL_WEBSITE.md) to clear unrelated program files while preserving the correct website `.git` folder. Open `site/index.html`, run `python tools/preview.py`, or use `PREVIEW_WEBSITE.bat` to preview. Publish directory remains **site**; no framework build or server dependency is added.

| Setting | Value |
| --- | --- |
| Website | https://www.mywavelink.com/ |
| Separate demo | https://demo.mywavelink.com/ |
| Sales | comercial@mywavelink.com |
| Product support | support@mywavelink.com |
| Publish directory | site |
| Existing build command | echo "Static site ready" |

## Validation

`python tools/check_site.py` checks local pages, links, anchors, assets, content and metadata. `python tools/check_http.py` compares local HTTP responses with source bytes. The optional `node tools/browser_smoke.cjs` uses Playwright/Chromium to check local-source rendering, seven categories, keyboard navigation, mobile menus, FAQs, clipboard handling, deep links, 200% text and no-JavaScript behavior. These tools are for review only; they are not deployed dependencies.

The browser script uses `playwright-core` or `playwright` already installed in the review environment. Set `BROWSER_EXECUTABLE` if using an existing Chromium executable. Its requests are fulfilled from local files at a synthetic HTTPS origin; it does not visit the live website or demo. Screenshots go into ignored `test-output` unless `QA_OUTPUT` is set. See [docs/VALIDATION.md](docs/VALIDATION.md).

## Content and source

The supplied website archive matches all 33 blobs of GitHub main **ea8ec477d6c4f699e09d34b293c315a2f1a5b5d8**. Application features were reviewed at **dd8eff975a594e41b10bf5e589577bcf4e954cee** (UI95), using its current and retained release documentation.

Interface examples use fictional records; they are not exact application screenshots. The public demo opens separately. Company sign-in, two-step verification and email alert wording now reflects the implemented application and its configuration requirements. This website does not enable those controls. See [docs/CONTENT_NOTES.md](docs/CONTENT_NOTES.md) and [docs/SECURITY_ROADMAP.md](docs/SECURITY_ROADMAP.md).

GitHub delivery status: read access verified; branch creation was rejected with 403 (Resource not accessible by integration). No remote commit, PR or deployment was made. Use the complete package with the existing GitHub Desktop workflow.
