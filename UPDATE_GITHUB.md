# Update Wavelink website to 2.3.1

**Contact update:** all website email links and displayed addresses now use **comercial@mywavelink.com**. The 2.3.0 design and complete-platform content are retained.

**This package is for `Wavelink-Website` only.** It must not replace the repository that runs `demo.mywavelink.com`.

## 1. Extract the ZIP

Choose **Extract All**. Open the `Wavelink-Website` folder inside the extracted package. You should see a `site` folder alongside `README.md`, `UPDATE_GITHUB.md`, `DEPLOYMENT.md`, `docs` and `tools`.

Open `site/index.html` to look at the design before publishing. The website is static: there is nothing to install on Render.

## 2. Open your existing repository

Go to your **Wavelink-Website** repository on GitHub. Work on the branch connected to the website deployment (previously `main`). Preserve a copy of the current site or note its current commit before replacing files, so the previous release can be restored if needed.

Do **not** create another demo service. Do **not** change the demo repository.

## 3. Upload the replacement files

From the **root of the website repository**, choose **Add file → Upload files**.

Drag the **contents** of the extracted `Wavelink-Website` folder into the upload area. Include the whole `site` folder, `docs`, `tools` and the root files. Existing paths should be replaced, and new files added in the same commit. Existing artwork is included so this is a complete package.

Do not upload the ZIP file itself. Do not upload the outer `Wavelink-Website` folder as an extra nested directory.

Correct:

```text
repository root
├── site
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── assets
├── README.md
└── ...
```

Incorrect:

```text
repository root
└── Wavelink-Website
    └── site
        └── index.html
```

Commit with a message such as **`Update Wavelink website 2.3.1 — business email`**. Follow your normal pull-request process when branch protection is enabled. GitHub's exact control labels may vary; preserving these file paths is the important part.

### GitHub Desktop alternative

In GitHub Desktop, select **Wavelink-Website** under **Current repository**, then use **Repository → Show in Explorer** to open its local folder. Check the current branch and fetch/pull any outstanding changes before editing. Copy the extracted package's contents into that folder and allow matching files to be replaced. Do not remove its `.git` directory. Review the changes, enter the summary **Update website contact email**, commit to your website branch, and select **Push origin**. No repository reset or force-push is needed.

## 4. Keep the existing website deployment settings

These values match the supplied website setup:

| Setting | Value |
| --- | --- |
| Service | Existing website **Static Site**, not the demo Web Service |
| Repository | `Wavelink-Website` |
| Branch | Your existing deployment branch, previously `main` |
| Root directory | Blank |
| Build command | `echo "Static site ready"` |
| Publish directory | `site` |

When automatic deployment is enabled, the new commit should trigger the website update. Otherwise deploy the latest website commit through your existing host's deployment control.

There is no need to change your domain records just to replace this website. Leave the `demo` DNS record, demo repository, demo Web Service and application environment variables unchanged.

## 5. Check the published website

After the host reports the website commit as deployed:

1. Open `https://www.mywavelink.com/` and use **Ctrl+F5** on Windows to request a fresh page. The headline should be **“Your whole operation. Working as one.”**
2. Check all **six permanent capability cards** under **More than individual tools. A connected operation.** Inventory and Manifests must still have separate, visible cards. Each detail link should select the matching product view. Try all **seven product tabs**; **Overview** should be selected on a fresh page load. Expand **Explore all platform capabilities** to see fourteen entries, then close it again.
3. Open the page on your phone, check the menu and expand an FAQ answer. Select **Open demo** and confirm it opens `https://demo.mywavelink.com/` separately.
4. Read the **Security & company access** section. Two-step verification and company-email sign-in must visibly say **Planned**; this website update does not enable either feature.
5. Test **Request a walkthrough**: your email application must address the draft to **comercial@mywavelink.com**. Check the company/security enquiry link, visible contact card, **Copy email** button, footer and **Privacy & website information** page. Every website contact must use that same address. Check that the long address wraps cleanly on a phone. No message is sent unless you send it yourself.

A mail link opens the visitor's configured email application; it is not an embedded contact form. Clipboard permissions vary; when copying is blocked the visible email address remains available for manual copying.

The complete ZIP replaces website 2.3.0, 2.2.0, 2.1.0 or 2.0.0 and also works as a full replacement for the earlier original website. No staged patch installation is necessary. It contains all artwork, assets, pages and source files.

## Restore the previous site

Restore the previous website commit through your normal Git workflow, or copy the saved previous website files back into the same repository and commit that restoration. Deploy that website commit. Do not alter the demo service as part of a website rollback.

## Important boundaries

This update does not confirm that your live deployment already matches these files. It does not change any DNS or hosting settings itself. The application previews are illustrative and labelled accordingly. Exact current host controls, DNS verification, custom-domain redirects, public demo availability and hosted 404 behaviour must be checked in your own deployed setup.
