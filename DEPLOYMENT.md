# Wavelink static website deployment

For an update to the existing repository, use [UPDATE_GITHUB.md](UPDATE_GITHUB.md). This file records the package's deployment requirements, rather than prescribing new DNS records.

## Architecture

```text
www.mywavelink.com   → existing website Static Site → Wavelink-Website/site

demo.mywavelink.com  → existing Wavelink application service (unchanged)
```

The public website links to the demo; it does not embed, proxy or initialise it. Demo controls open a separate tab with `noopener noreferrer`. No login details, public gateway settings, database exports or application source are bundled.

## Static host configuration

The package preserves the values documented in the supplied website:

- Repository root: the directory containing `site`, `README.md` and `DEPLOYMENT.md`.
- Root directory setting: blank.
- Build command: `echo "Static site ready"`.
- Publish/output directory: `site`.
- Deployment branch: the existing connected branch (previously `main`).

There is no `npm install`, framework build, Node server, Python service, database or secret required. The `tools` folder is for optional local review and tests and should not be the publish directory.

## Domains

Canonical home URL: `https://www.mywavelink.com/`.
Demo destination: `https://demo.mywavelink.com/`.

Keep working domain records for this update. The source archive's historical DNS setup instructions have deliberately not been repeated as current provider instructions. For any separate domain migration, use the actual targets displayed by your host and DNS provider. Do not change `demo`, email/MX or unrelated records to publish a visual website update.

The root-domain to `www` redirect is a hosting/DNS concern. The website files do not configure or verify that redirect.

## Caching and file paths

Keep the full `site/assets` folder. HTML loads CSS and JS with `?v=2.3.1`; increase this value in HTML whenever those assets are changed for a future release. The shared stylesheet and script work without a bundler.

`404.html` uses root-relative asset paths so a host can serve it for deep missing URLs. The package includes the page but does not configure provider-specific rewrite rules. Check the deployed site's missing-page behaviour; do not add a catch-all SPA rewrite to `index.html` for this static site.

## Contact, privacy and content

Email contact is `mailto:` only. The clipboard button copies the displayed address after an explicit click; denied permission displays a manual-copy message. No customer data is collected by an on-site form.

The website code has no analytics, advertising, tracking cookies or browser storage. Provider-level logs and the separate demo application are outside this statement. Review the supplied privacy/site-information text against your actual deployment before adding analytics, forms or other services.

The share image is a screenshot-derived preview of this website, using the original provided imagery. Actual social-platform cache behaviour was not verified.

## Security feature boundaries

The security section is product and roadmap copy, not authentication code. Publishing it does not enable company-email sign-in, single sign-on, two-step verification, encryption policies or changes to demo permissions. Confirm customer-specific controls separately with the application release and IT deployment review. Do not publish company credentials or identity-provider secrets in this static repository. See [docs/SECURITY_ROADMAP.md](docs/SECURITY_ROADMAP.md).

## Test scope

See [docs/VALIDATION.md](docs/VALIDATION.md). This repository package has been checked locally. No GitHub push, hosting deployment, domain verification or external availability test was performed.
