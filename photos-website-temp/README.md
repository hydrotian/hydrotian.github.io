# Tian Zhou - Photography Portfolio

A modern, fast photography portfolio website built with SvelteKit and Tailwind CSS.

## Features

- 🚀 **Blazing Fast**: Static site generation with SvelteKit
- 📱 **Responsive**: Works beautifully on all devices
- 🎨 **Clean Design**: Minimalist gallery layout
- 🏷️ **Categories**: Filter photos by landscape, street, nature
- 📸 **Photo Details**: Display EXIF data, location, and description
- 🌐 **GitHub Pages**: Free hosting

## Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Adding New Photos

1. Add your photo images to `static/images/` directory
2. Create thumbnail versions (recommended: 600x600px)
3. Update the photos array in `src/routes/+page.ts`

### Photo Entry Format

```typescript
{
  slug: 'unique-slug',
  title: 'Photo Title',
  date: '2024-01-15',
  location: 'Location Name',
  category: 'landscape' | 'street' | 'nature',
  thumbnail: 'images/photo-thumb.jpg',
  image: 'images/photo.jpg',
  description: 'Optional description',
  camera: 'Optional camera info',
  lens: 'Optional lens info',
  settings: 'Optional camera settings'
}
```

## Image Optimization

For best performance, optimize your images:

- **WebP format**: 25-30% smaller than JPEG
- **Thumbnails**: ~600x600px, ~100-200KB
- **Full images**: ~2000px wide, ~200-500KB

Use tools like:
- [Squoosh](https://squoosh.app/) for WebP conversion
- ImageMagick: `convert input.jpg -quality 85 output.webp`

## Deployment

The site automatically deploys to GitHub Pages when you push to the `main` branch.

1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. Push to main branch

Your site will be available at: `https://hydrotian.github.io/photos/`

## Structure

```
photos/
├── src/
│   ├── routes/
│   │   ├── +layout.svelte       # Main layout with nav/footer
│   │   ├── +page.svelte         # Gallery grid
│   │   ├── +page.ts             # Photo data
│   │   ├── photo/[slug]/        # Individual photo pages
│   │   └── about/               # About page
│   ├── app.css                  # Tailwind styles
│   └── app.html                 # HTML template
├── static/
│   ├── images/                  # Your photos go here
│   └── .nojekyll                # GitHub Pages config
└── package.json
```

## License

© 2024 Tian Zhou. All rights reserved.
