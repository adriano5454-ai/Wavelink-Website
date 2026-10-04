# Apply website 3.0.0

Use the existing **adriano5454-ai/Wavelink-Website** repository. This release updates the marketing website only.

1. Copy the package contents into your website checkout, replacing matching paths. Keep `.git` and independent files. If the GitHub main branch has advanced from `ea8ec477d6c4f699e09d34b293c315a2f1a5b5d8`, reconcile the newer changes first.
2. Review the website locally: open `site/index.html`, run `python tools/preview.py`, or use the Windows preview launcher.
3. Commit and push through your normal GitHub workflow, or review and merge the prepared website pull request if available.
4. Use the existing static host with publish directory **site** and the existing build command `echo "Static site ready"`.
5. After deployment, check the home page on desktop and phone, switch all seven product categories, open the capability directory, follow Imports, and check the demo and sales email destinations. Check `/privacy.html` and the host’s normal missing-page behavior.

The package preserves the existing public website domain, separate demo destination and static hosting approach. CSS and JavaScript use cache version **3.0.0**. The application repository is not part of this website update.
