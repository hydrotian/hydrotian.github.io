# CLAUDE.md

This is a lightweight academic website built with Jekyll using the Minimal Mistakes theme, hosted on GitHub Pages.

## Project Overview

- **Type**: Academic portfolio website
- **Owner**: Tian Zhou (SimHydro)
- **Framework**: Jekyll static site generator
- **Theme**: Minimal Mistakes (forked from academicpages template)
- **Hosting**: GitHub Pages
- **URL**: <https://simhydro.com>

## Project Structure

- `_config.yml` - Main Jekyll configuration
- `_pages/` - Static pages (about, cv, publications, etc.)
- `_publications/` - Individual publication markdown files
- `_talks/` - Conference talks and presentations
- `_slides/` - Slide presentations
- `_includes/` - Reusable template components
- `_layouts/` - Page layout templates
- `_sass/` - SCSS stylesheets
- `assets/` - CSS, JS, fonts, and other static assets
- `images/` - All image files including papers, photos, profiles
- `files/` - PDF and other downloadable files
- `markdown_generator/` - Python scripts for generating markdown from data

## Development Commands

### Local Development

```bash
# Install dependencies
bundle install

# Serve locally with live reload
bundle exec jekyll serve

# Serve with development config
bundle exec jekyll serve --config _config.yml,_config.dev.yml

# Clean build directory
bundle exec jekyll clean
```

### Build Commands

```bash
# Build site for production
bundle exec jekyll build
```

### Content Management

```bash
# Generate publications from data
cd markdown_generator
python publications.py

# Generate talks from data
python talks.py
```

## Key Features

- Responsive academic portfolio layout
- Publication list with images and links
- Talk/presentation archive
- CV page with downloadable PDF
- Photo galleries and slide presentations
- SEO optimization
- Google Analytics integration

## Content Guidelines

- Publications are stored as individual markdown files in `_publications/`
- Each publication should have a corresponding image in `images/papers/`
- Talk abstracts go in `_talks/` with optional slides in `_slides/`
- Profile images are stored in `images/` with multiple resolutions
- CV PDF should be updated in `files/CV_Zhou.pdf`

## Deployment

- Site automatically builds and deploys via GitHub Pages
- Push to master branch triggers rebuild
- Custom domain configured via CNAME file

## Theme Customization

- Main styles in `_sass/` directory
- Custom includes in `_includes/`
- Site-wide settings in `_config.yml`
- Navigation configured in `_data/navigation.yml`

## Maintenance Notes

- Ruby dependencies managed via Gemfile
- Regular updates needed for security patches
- Jekyll 3.x compatible theme