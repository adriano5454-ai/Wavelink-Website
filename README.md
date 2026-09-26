# Wavelink website 2.3.1

**Your whole operation. Working as one.**

Complete static marketing website for **Wavelink by AJ Offshore Solutions**. This contact-only release updates every website email reference to **comercial@mywavelink.com** and preserves the 2.3.0 full-platform story: equipment, logistics, maintenance, people, safety and daily work. Inventory and manifests remain named, permanent first-row capabilities; they no longer define the entire product.

## Publish this package

Follow [UPDATE_GITHUB.md](UPDATE_GITHUB.md). Upload the contents of this folder to the existing **Wavelink-Website** repository, replacing matching paths. Publish **`site`** using the existing static-site setup. Do not replace the separate demo application's repository.

```text
Wavelink-Website/
├── site/                 Public website and locally bundled images
├── docs/                 Content boundaries, security roadmap and test reports
├── tools/                Optional local preview / validation scripts
├── UPDATE_GITHUB.md      Upload guide
├── DEPLOYMENT.md         Existing static-host requirements
└── PREVIEW_WEBSITE.bat   Optional Windows local-preview launcher
```

## What changed in 2.3.1

All walkthrough and company-contact links, visible contact addresses, copy-email data, privacy-page contact details, documentation and automated contact checks now use **comercial@mywavelink.com**. Existing email subjects are preserved. No mailbox, DNS, hosting, demo or application authentication setting is changed.

## Full-platform design retained from 2.3.0

- The opening presents a complete operations platform rather than an inventory-only system.
- A six-area illustration immediately names equipment/logistics, maintenance/readiness, people/continuity, safe working, daily operations and company control.
- Six permanent capability cards give visitors the breadth before they interact: Inventory; Manifests; Maintenance & certificates; Handovers & tasks; Safety & team checks; Fleet, logs & planning.
- A shared foundation covers users, departments, permissions, project data and deployment.
- The product explorer now opens on **Overview**, followed by six detailed views. Inventory and Manifests still have separate tabs.
- Four fictional records illustrate the wider context: a manifest, equipment readiness, a team check and a saved handover. This is not a live dashboard or an automatic workflow.
- Fourteen expanded capability entries include tasks, fault reports and HSE / QSHE, without displaying every description by default.
- Collaboration, FAQ, contact and social-preview wording now represent the whole operation.
- Two-step verification and company-email sign-in retain explicit **Planned** labels. Universal vessel isolation, certifications, SSO and production security are not implied.

## Preserved configuration

| Item | Value |
| --- | --- |
| Public canonical URL | `https://www.mywavelink.com/` |
| Separate demo | `https://demo.mywavelink.com/` |
| Contact | `comercial@mywavelink.com` |
| Publish directory | `site` |
| Build command | `echo "Static site ready"` |
| Framework/server dependency | None |

No npm build, application server, database, API key or secret is needed. Python and Playwright are optional local-review tools, not deployed website dependencies.

## Local review

Open `site/index.html` directly, or run `python tools/preview.py` / `PREVIEW_WEBSITE.bat` when Python is installed. The website uses system fonts and local assets. Tabs use manual keyboard activation: arrow keys/Home/End move focus; Enter/Space select. Without JavaScript, the six-area overview, default product view, full capability directory, navigation and FAQs remain available.

```text
python tools/check_site.py
python tools/check_http.py
python tools/browser_smoke.py
```

The optional browser test needs the Python `playwright` package and Chromium in the reviewer’s environment. An already installed browser can be selected with `--browser /path/to/chromium`. The static site itself needs none of these tools. Restricted environments can use `--in-memory`; that mode tests rendering and interaction, not browser navigation. See [docs/VALIDATION.md](docs/VALIDATION.md) for the exact tests performed here and their limits.

## Source and status

Prepared 26 September 2026 UTC from **Wavelink_Website_2.3.0_GitHub.zip**, SHA-256 `2fa0f07be43c3b60f310bf3843d7385932bbd5530ff7e90e8f30710ca540afba`. All **32** parent manifest records were verified against the extracted bytes before editing. This is website versioning, separate from Wavelink application versions.

No application code was supplied or audited in this revision. Product coverage follows the established project scope and previous website, with exact module/workflow availability to be confirmed in a company walkthrough. No GitHub push, deployment, DNS update or authentication change was made.

Read [docs/CONTENT_NOTES.md](docs/CONTENT_NOTES.md) and [docs/SECURITY_ROADMAP.md](docs/SECURITY_ROADMAP.md) before extending marketing claims or changing roadmap labels.
