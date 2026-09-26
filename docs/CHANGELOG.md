# Website 2.3.0 — 26 September 2026 UTC

**Whole-platform positioning, with inventory and manifests kept prominent.**

- Replace the inventory-only headline/hero with “Your whole operation. Working as one.”
- Replace the two-module core section with six always-visible capability groups and a shared people/access/data foundation.
- Add a default Overview product view; keep separate Inventory and Manifests tabs and broaden the other four views.
- Expand the capability directory to fourteen groups, including task responsibilities, fault reports and HSE / QSHE.
- Broaden collaboration, FAQ, contact and social-preview messaging.
- Qualify vessel-specific access by supported module; retain explicit planned authentication labels.
- Preserve static hosting paths, brand assets, domain/demo/contact destinations and the separate application.
- Update local tests for the wider default, all seven tabs and all fourteen capabilities.
- Add a positioning checkpoint to avoid narrowing the whole product around one module in later edits.

No remote changes or application/authentication implementation included.

---

# Website release history

## 2.2.0 — 26 September 2026 (UTC)

Inventory and manifests promoted to the primary website story. New headline: “Inventory. Manifests. One team.” Updated navigation, hero product illustration, visible core summaries, dedicated Inventory and Manifests panels, default Inventory selection, team responsibilities, FAQs, contact copy, metadata and sharing image.

Inventory examples now show stock, quantity, low-stock status, boxes/contents, QR verification, location, certificates, maintenance and movement history. Manifest examples keep the same equipment IDs through dispatch, confirmed receipt and distinct final placement, with an attached-document illustration.

Six local capability panels; detail links activate the correct panel with keyboard focus. Twelve capability groups and broader operational coverage retained. Security and corporate-email/two-step-verification planned labels retained. No app changes, authentication implementation, deployment, DNS or remote Git changes.

Updated checks assert both core sections are visible without tab interaction and Inventory is selected by default. Parent ZIP and 30 parent manifest entries verified. Exact test scope is recorded in VALIDATION.md.

---

# Website 2.1.0 — 25 September 2026

## Collaboration, product coverage and company security

Replaced the small hero workflow widget and five-stage asset journey with a team-led hero and a larger five-area capability showcase. Added a twelve-group expandable capability directory, a dedicated crews/supervisors/shore-team story, and an enterprise evaluation contact path.

Added a prominent security section: role-aware access and accountable working are separated from planned two-step verification and company-email access. Explicit future-status labels, an FAQ and a security roadmap document avoid implying that website publication implements authentication or proves a production security posture. Corporate SSO/provider integration remains a separate requirements discussion.

Retained the static deployment structure, canonical/demo URLs, contact details, artwork, progressive enhancement, mobile navigation, keyboard-operated manual tabs, copy-email fallback and no-tracker/no-storage behaviour. Updated metadata, social preview, supporting pages, upload instructions and validation tooling for this release.

The product views remain clearly labelled fictional illustrations, not exact screenshots or a real-time app feed. No application, account, database, gateway, DNS, repository or hosting change was performed.

---

# Website 2.0.0 — 25 September 2026

This version number belongs to the marketing website, not the Wavelink application.

## Design and story

Replaced the long, predominantly descriptive landing page with a clearer introduction, consistent maritime colours, stronger heading hierarchy, refined spacing and a grouped capability layout. Preserved AJ Offshore Solutions branding, the original image and brand marks, and the distinction between the public website and the application demo.

## Interactions

Added three switchable fictional product illustrations (Handovers, Assets, Logistics), and five selectable stages in a fictional asset journey (Receive, Locate, Move, Maintain, Handover). Keyboard users can move between tab controls with Left/Right, Home and End, then activate with Enter/Space. No carousel timer or forced motion was added.

Improved mobile navigation with Escape closing and focus handling. Added a native details/summary FAQ and direct email contact with a copy action and permission-failure fallback.

## Content and deployment

Expanded the explanations of handovers, equipment history, maintenance/certificates, manifests, permissions, checklists, toolbox talks, logs and supporting project tools. Distinguished hosted deployment from a Windows hub on a local network; did not promise automatic cross-deployment synchronisation or independent disconnected-phone operation.

Preserved `site` as the publish folder and all demo destinations as `https://demo.mywavelink.com/`. Added a privacy/site-information page, a 404 document, social sharing metadata and image, raster icons, an optimised small-screen image, validation tools, upload instructions and file provenance.

## Unchanged boundaries

No changes to the application, authentication, public demo gateway, database, backend, DNS, hosting configuration, or actual deployed repository. No customer metrics, testimonials or real client project examples were added. No new external runtime dependencies, trackers, fonts, API keys or form services.
