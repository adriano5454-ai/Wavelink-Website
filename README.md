# Wavelink website

The public landing page for Wavelink by AJ Offshore Solutions. This is a standalone static website for `www.mywavelink.com`. Its demo buttons open the existing application at `https://demo.mywavelink.com/`.

## Repository layout

```text
Wavelink-Website/
├── site/
│   ├── assets/
│   │   ├── favicon.svg
│   │   ├── offshore-operations.webp
│   │   └── wavelink-mark.svg
│   ├── index.html
│   ├── robots.txt
│   ├── script.js
│   ├── sitemap.xml
│   └── styles.css
├── .gitignore
├── DEPLOYMENT.md
└── README.md
```

There is no package manager, framework, API key, database, or build dependency. The Render publish directory is **`site`**.

## Preview locally

You can open `site/index.html` in a browser. For a server-style preview, from the repository folder run:

```powershell
py -m http.server 8000 -d site
```

Then open `http://localhost:8000/`. Stop the server with `Ctrl+C`. The Python command is optional for publishing.

## Edit the page

- Text and links: `site/index.html`
- Colours, layout, responsive behaviour: `site/styles.css`
- Mobile navigation: `site/script.js`
- Mark and favicon: `site/assets/*.svg`
- Offshore image: `site/assets/offshore-operations.webp`

All demo buttons point to `https://demo.mywavelink.com/`. The walkthrough email uses `adriano5454@gmail.com`; change this in `site/index.html` if you set up a business mailbox.

The interface illustration uses fictional data and is labeled as illustrative on the page. The offshore image was generated for this website. It is not a photograph of a client vessel. No customer names, client records, demo credentials, tracking scripts, or third-party fonts are included.

## Publish

Follow [DEPLOYMENT.md](DEPLOYMENT.md) for the complete GitHub, Render and DNS setup. Keep the demo repository, demo Render Web Service, and `demo` DNS record separate.

Copyright © 2026 AJ Offshore Solutions. All rights reserved.
