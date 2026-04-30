# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic portfolio site for Tian Zhou (SimHydro), built with Jekyll using a forked academicpages / Minimal Mistakes theme and deployed via GitHub Pages at <https://simhydro.com>. The `master` branch is the deploy branch — pushes trigger a GitHub Pages rebuild. Custom domain is set via `CNAME`.

## Development

```bash
# Install Ruby deps
bundle install

# Serve locally (production-like config)
bundle exec jekyll serve

# Serve with dev overrides (disables analytics, sets url=localhost:4000)
bundle exec jekyll serve --config _config.yml,_config.dev.yml

bundle exec jekyll build
bundle exec jekyll clean
```

If `bundle install` fails after pulling, the README's recommended fix is to delete `Gemfile.lock` and re-run.

## Content Architecture

Content lives in Jekyll collections, each rendered into a list page under `_pages/`:

- `_publications/` — one markdown file per paper. Permalink pattern `/publication/YYYY-slug`. Each entry typically references an image in `images/papers/` and may set `comments: true` to enable Giscus.
- `_talks/` — talk/presentation entries.
- `_slides/` — slide deck pages (with companion files in top-level `slides/`).
- `_pages/` — static pages (about, cv, publications index, etc.).
- `_data/navigation.yml` — site nav.
- `_includes/`, `_layouts/`, `_sass/` — theme overrides.
- `files/CV_Zhou.pdf` — the linked CV download; replace this file to update the CV.

## Publication Generation — Two Workflows

There are two parallel toolchains for producing `_publications/` markdown. **Prefer the ORCID manager for new work**; the CSV tool is legacy.

### 1. ORCID manager (current)

`orcid_publications_manager.py` (top-level) syncs from ORCID ID `0000-0003-1582-4005`, diffs against existing `_publications/`, and only creates files for missing papers. It writes to `.orcid_cache.json` to avoid re-fetching. See `ORCID_MANAGER_README.md` for the full workflow including Giscus comments setup.

```bash
pip3 install -r requirements.txt   # requests, PyYAML
python3 orcid_publications_manager.py
# rm .orcid_cache.json   # force full refresh
```

Generated entries include `comments: true`; the Giscus integration lives under `_includes/comments-providers/` and is configured via the `giscus:` block in `_config.yml`.

### 2. CSV/notebook generator (legacy)

`markdown_generator/` contains the original academicpages workflow (`publications.py`, `talks.py`, plus Jupyter notebooks and `add_new_pub_here.csv` / `talks.tsv`). Still functional for talks; for publications, treat as superseded by the ORCID manager.

## Conventions

- Publication images: `images/papers/YEAR-slug.png`, referenced from the publication's frontmatter.
- When adding a publication by hand, match the frontmatter shape used by ORCID-generated files (title, collection, permalink, excerpt, date, venue, paperurl, citation).
- Site-wide settings (author info, analytics, Giscus IDs, social links) all live in `_config.yml`. Do not duplicate them into individual pages.
