# Publish Wavelink at www.mywavelink.com

This guide assumes the hosted demo already works at `https://demo.mywavelink.com/`. The landing page gets its **own GitHub repository and Render Static Site**. Your demo Web Service remains as it is.

## 1. Extract and check the package

Download the `Wavelink-Website.zip` file and choose **Extract All** on Windows. Open the resulting `Wavelink-Website` folder. You should see `README.md`, `DEPLOYMENT.md` and a `site` folder. Open `site/index.html` to preview it locally.

When uploading to GitHub, upload the **contents of the extracted `Wavelink-Website` folder**. Do not upload the ZIP file as a single repository file. GitHub should display `site`, `README.md`, and `DEPLOYMENT.md` at the repository root; `site/index.html` must stay inside `site`.

## 2. Create the GitHub repository

1. Sign in to [GitHub](https://github.com/) and open [New repository](https://github.com/new).
2. Name it **`Wavelink-Website`**. Select your own account or AJ Offshore Solutions organization as owner. A private repository is fine if Render has access to it.
3. Leave **Add a README**, `.gitignore`, and **license** unchecked because the package already contains its own files.
4. Select **Create repository**.
5. On the empty repository page, choose **uploading an existing file** (or **Add file → Upload files**).
6. Drag the extracted folder's **contents**, including the `site` folder and its files, into the upload area. Commit the upload to the `main` branch with a message such as `Add Wavelink landing page`.
7. Confirm GitHub shows `site/index.html` and `site/assets/offshore-operations.webp` in the new repository.

If your browser does not preserve the `site` folder when uploading, use [GitHub Desktop](https://desktop.github.com/) or Git instead. Do not put the marketing files in your existing demo repository.

### Optional Git command route

Create the empty repository on GitHub as above, then run these commands inside the extracted `Wavelink-Website` folder. Replace `<YOUR-ACCOUNT>` with the actual GitHub owner:

```powershell
git init
git add .
git commit -m "Add Wavelink landing page"
git branch -M main
git remote add origin https://github.com/<YOUR-ACCOUNT>/Wavelink-Website.git
git push -u origin main
```

## 3. Create a new Render Static Site

1. Sign in to the [Render Dashboard](https://dashboard.render.com/).
2. Choose **New → Static Site**, then connect the new `Wavelink-Website` repository. If GitHub asks which repositories Render may access, include this new repository.
3. Set the service name to something like **`wavelink-website`** and branch to **`main`**.
4. Use these settings:

   | Setting | Value |
   | --- | --- |
   | Service type | Static Site |
   | Root Directory | Leave blank |
   | Build Command | `echo "Static site ready"` |
   | Publish Directory | `site` |
   | Auto Deploy | On |

5. Choose **Create Static Site** and wait for the first successful deploy. Open the new `https://<YOUR-SITE>.onrender.com/` address shown by Render. The Wavelink landing page should appear. Test **Explore the live demo** to confirm it opens `https://demo.mywavelink.com/`.

Keep the new Static Site distinct from the existing demo Web Service. Never change the demo service's publish settings or repository to these values.

## 4. Add www.mywavelink.com in Render

1. Open the **new Static Site** in Render, then **Settings → Custom Domains → Add Custom Domain**.
2. Add **`www.mywavelink.com`**. Render currently adds the corresponding root domain, `mywavelink.com`, and redirects that root address to `www`.
3. Render will show the DNS values needed for verification. Keep that screen open while changing your DNS provider's records.

## 5. Update your domain DNS

Sign in wherever your `mywavelink.com` DNS is managed. The exact controls vary by provider. Point **only the landing-page hosts** to the new Static Site:

| Host/name | Type | Value/target |
| --- | --- | --- |
| `www` | CNAME | The **new website** `...onrender.com` hostname shown in Render |
| `@` (root) | ALIAS/ANAME, if supported | The same **new website** `...onrender.com` hostname |
| `@` (alternative) | A | `216.24.57.1` (Render's documented root-domain IP), if your provider has no ALIAS/ANAME |

Use **one** root-domain approach that your DNS provider supports. Confirm the IP against Render's live instructions before entering it. Cloudflare's root setup uses a flattened CNAME instead; follow Render's Cloudflare instructions if Cloudflare manages your DNS. Remove old conflicting `www`/root entries if necessary, and remove conflicting `AAAA` records for those hosts as Render instructs. Do not remove the `demo` CNAME/A record, MX/email records, or unrelated DNS entries.

The `www` CNAME must target the new **Static Site**, not the existing demo service. The `demo` record must continue targeting the existing **demo Web Service**.

## 6. Verify the domains

1. Back in the new Render Static Site's **Custom Domains** section, click **Verify**. DNS changes can take some time to propagate; if pending, try again later.
2. Wait for Render's TLS certificate, then check:

   | Address | Expected result |
   | --- | --- |
   | `https://www.mywavelink.com/` | New Wavelink landing page |
   | `https://mywavelink.com/` | Redirects to `www.mywavelink.com` |
   | `https://demo.mywavelink.com/` | Existing Wavelink demo |
   | Landing page **Explore live demo** buttons | Open the existing demo |

Render's included custom-domain allowance varies by plan. With `demo`, `www`, and the root domain, check the Render Dashboard for any additional-domain charge before completing your setup.

## 7. Make later edits

Edit the files in the **new website repository** and commit to `main`. Render will deploy the updated landing page automatically. Changing the website does not require redeploying the demo app.

Before announcing the site, you may want to replace the walkthrough email in `site/index.html` with a dedicated Wavelink business address. The current link uses the known AJ Offshore Solutions support contact. The asset view and vessel photo are explicitly illustrative; replace them with approved real product screenshots or company images whenever you have them.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Render page is blank or 404 | **Publish Directory** is `site`, and `site/index.html` exists in GitHub. |
| Image or styling missing | Keep the `site/assets` folder and all files under `site`; do not upload only `index.html`. |
| Domain verification pending | Compare DNS against Render's displayed values; remove conflicting old or `AAAA` records for `www`/root; allow propagation. |
| `www` opens the demo | `www` points to the new website's `onrender.com` address, not the demo service. |
| Demo stops opening | Restore/check the existing `demo` DNS record and the original demo Render Web Service; the new site never needs its settings. |

Official references: [Render Static Sites](https://render.com/docs/static-sites), [Render custom domains](https://render.com/docs/custom-domains), [Render DNS setup](https://render.com/docs/configure-other-dns), [GitHub create a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository), [GitHub upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
