# Wavelink static website deployment

The existing marketing site publishes **Wavelink-Website/site** at https://www.mywavelink.com/. The separate application demo remains linked at https://demo.mywavelink.com/.

## Static host settings

| Setting | Value |
| --- | --- |
| Root directory | Blank / repository root |
| Build command | echo "Static site ready" |
| Publish directory | site |
| Usual deployment branch | main |

No npm build, app server, database or secret is required. Review tools are optional and stay outside the publish directory. Existing DNS, mail, demo and application settings do not need a change for this website update.

All deployed assets are local. HTML loads `styles.css` and `script.js` with `?v=3.0.0`. Keep the complete `site/assets` folder. The 404 page uses root-relative assets; confirm the existing host’s missing-page behavior without adding an SPA catch-all redirect.

Contact is by `mailto:`. No on-site form, analytics, browser storage or tracking code was added. The copy-email control writes only the visible address after a click. Provider-level request logs remain outside the website code.

The product explorer changes only fictional examples in the page. It does not connect to the application API, upload documents, sign records, or alter the demo. Application security and mail features require separate company setup; see [docs/SECURITY_ROADMAP.md](docs/SECURITY_ROADMAP.md).

See [docs/VALIDATION.md](docs/VALIDATION.md) for local acceptance. A GitHub update and a live hosting deployment are distinct states; verify the intended commit through the existing host after publication.
