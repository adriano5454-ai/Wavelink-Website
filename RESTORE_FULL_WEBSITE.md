# Restore the complete Wavelink website — 3.0.0

This folder is the **complete updated Wavelink-Website source**, including all public pages, artwork/assets, styles, JavaScript, documentation and review tools. It is suitable for replacing a website checkout contaminated with Wavelink application files. It does not require any earlier patch.

## Replace the local website contents

1. In GitHub Desktop, select **Wavelink-Website**. Use **Repository → Show in Explorer** to open its actual repository folder. Verify **Repository settings → Remote** points to `https://github.com/adriano5454-ai/Wavelink-Website` (optionally ending in `.git`).
2. Close any editor using the folder. Copy the entire current website repository folder to a separate backup location.
3. In the original website repository folder, remove **all contents except its existing `.git` folder**. Enable Explorer’s hidden-item display so you can preserve `.git`. This removal is what clears application files that an ordinary overwrite would leave behind.
4. Extract this ZIP elsewhere. Copy **everything inside its `Wavelink-Website` folder** into the original, now-empty website repository folder. Copy the contents, not the enclosing folder; `site` must sit directly at the repository root.
5. Preview by opening `site/index.html`. In GitHub Desktop review both additions/changes and deletions. Commit all recovery changes, then **Push origin**. A push includes deleting tracked application files removed in step 3.
6. Keep the existing Render static-site configuration: publish directory **site**, existing build command `echo "Static site ready"`. After deployment, check the home page, tabs, Imports, demo link and contact links.

If GitHub Desktop shows the application repository as the remote, or repository metadata was also overwritten, **clone `adriano5454-ai/Wavelink-Website` into a fresh folder first**. Then perform the same clean replacement in that clone, preserving the clone’s correct `.git`. A contaminated remote checkout still needs step 3.

## Expected website folders

- `site`: the public website, including `assets`.
- `docs`: content, source and validation notes.
- `tools`: optional preview and validation helpers.

The remaining repository-root files are website documentation, the Windows preview launcher and `.gitignore`. The package contains no application `deploy`/`vendor` folders, Dockerfile, database, demo fixtures or application installer. Its `.git` history is not included; retain the website checkout’s correct metadata.

Website version remains **3.0.0**, with the previously verified UI95 feature content and responsive design. This recovery package changes the replacement instructions; public site content is unchanged. The application repository and its services are separate.

## Current GitHub check

At website main commit `6dc2544cd620badd34d3c1f8282495d08e93b224`, 46 files were present. The following remote paths are absent from this clean website package and are removed by the clean replacement procedure:

- `DELIVERY_CHECKS.json`
- `DEPLOYMENT_FILES.json`
- `Dockerfile`
- `START_HERE.html`
- `deploy/apply_ui96.py`
- `docs/CONTINUATION_CHECKPOINT.md`
- `docs/DEVELOPMENT_TODO.md`
- `docs/UI96_REVIEW_REPORT.json`
- `docs/UI96_SOURCE_PROVENANCE.json`
- `docs/WORKSPACE_UI96.md`
- `tests/README.md`
- `tests/test_ui96_build.py`

The clean website files also replace any contaminated file with a matching path. No remote cleanup was performed here.
