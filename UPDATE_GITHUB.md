# Install the full clean website repository — 3.0.0

For this recovery use [RESTORE_FULL_WEBSITE.md](RESTORE_FULL_WEBSITE.md). This is a complete website repository snapshot, not a changed-files patch.

Make a backup of the actual **Wavelink-Website** checkout, verify its remote, and remove all working-tree contents except the correct `.git`. Then copy everything inside this package’s `Wavelink-Website` folder into that checkout. The clean replacement removes unrelated application files that an overwrite alone would preserve. Review and commit deletions together with the restored website files, then push through GitHub Desktop.

Preview with `site/index.html` or `PREVIEW_WEBSITE.bat`. The public `site` folder must sit directly at the repository root. The existing static host still publishes **site** using `echo "Static site ready"`.

This package retains the public site’s existing demo/contact destinations and updated 3.0.0 design. It makes no application/database or hosting-setting change. It includes no `.git` folder or GitHub credentials.
