# ORCID Publications Manager

A modern replacement for the CSV-based `markdown_generator` tool that automatically syncs publications from your ORCID profile to your Jekyll academic website.

## Features

✅ **Automatic ORCID Sync**: Fetches publications directly from ORCID API  
✅ **Smart Diff Detection**: Only creates new publications, doesn't duplicate existing ones  
✅ **Auto-Generated Descriptions**: Creates publication summaries automatically  
✅ **Comments System**: Adds Giscus comments to each publication  
✅ **Image Placeholders**: Provides template for adding publication images  
✅ **Caching**: Avoids unnecessary API calls with intelligent caching  

## Quick Start

### 1. Install Dependencies

Choose one of these methods:

**Option A: Virtual Environment (Recommended)**
```bash
python3 -m venv orcid_env
source orcid_env/bin/activate
pip install requests PyYAML
```

**Option B: User Installation**
```bash
pip3 install --user requests PyYAML
```

**Option C: System Installation (if needed)**
```bash
pip3 install --break-system-packages requests PyYAML
```

### 2. Setup Giscus Comments (Optional)

To enable comments on publication pages:

1. **Enable GitHub Discussions**:
   - Go to your repository settings: https://github.com/hydrotian/hydrotian.github.io/settings
   - Under "Features", check ✅ "Discussions"

2. **Install Giscus App**:
   - Visit: https://github.com/apps/giscus
   - Click "Install" and select your repository

3. **Configure Giscus**:
   - Go to: https://giscus.app/
   - Enter repository: `hydrotian/hydrotian.github.io`
   - Choose settings and copy the configuration values

4. **Update `_config.yml`**:
   ```yaml
   giscus:
     repo_id: "YOUR_REPO_ID_HERE"        # From giscus.app
     category_id: "YOUR_CATEGORY_ID_HERE" # From giscus.app
   ```

### 3. Run the Manager

```bash
python3 orcid_publications_manager.py
```

The script will:
- Fetch all publications from your ORCID profile (0000-0003-1582-4005)
- Compare with existing Jekyll publications
- Create new publication pages for any missing papers
- Enable comments on each publication
- Cache results to avoid repeated API calls

### 4. Review and Commit

```bash
# Review new publications
ls _publications/

# Add publication images (optional)
# Copy images to images/papers/ and update the markdown files

# Commit changes
git add .
git commit -m "Sync publications from ORCID"
git push
```

## File Structure

```
├── orcid_publications_manager.py    # Main script
├── setup_orcid_manager.py          # Setup helper
├── requirements.txt                 # Python dependencies
├── .orcid_cache.json               # Cache file (created automatically)
├── _publications/                   # Generated publication pages
├── _includes/comments-providers/    # Giscus integration
└── images/papers/                  # Publication images
```

## Publication Page Format

Each generated publication includes:

```yaml
---
title: "Paper Title"
collection: publications
permalink: /publication/2023-paper-title
excerpt: 'AI-generated description of the paper...'
date: 2023-01-01
venue: 'Journal Name'
paperurl: 'https://doi.org/...'
citation: 'Full citation...'
comments: true  # Enable comments
---
```

## Configuration

### ORCID Settings
- **ORCID ID**: Currently set to `0000-0003-1582-4005`
- Edit `ORCID_ID` in `orcid_publications_manager.py` to change

### Publication Directory
- **Default**: `_publications/`
- Edit `PUBLICATIONS_DIR` to change location

### Image Placeholders
- **Directory**: `images/papers/`
- **Format**: `YEAR-paper-title.png`
- Uncomment image lines in generated markdown files after adding images

## Advanced Usage

### Dry Run Mode
To see what would be created without making changes:
```python
# Add this at the top of orcid_publications_manager.py
DRY_RUN = True  # Set to False for actual execution
```

### Custom Descriptions
The script generates basic descriptions automatically. To enhance with AI-generated descriptions, you can integrate with OpenAI API or similar services by modifying the `generate_publication_description()` method.

### Scheduling
Add to cron for automatic updates:
```bash
# Run weekly on Sundays at 2 AM
0 2 * * 0 cd /path/to/your/site && python3 orcid_publications_manager.py
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'requests'"**
- Solution: Install dependencies as shown in Step 1

**"No works found or failed to fetch from ORCID"**
- Check internet connection
- Verify ORCID profile is public
- Check ORCID API status

**"Comments not showing up"**
- Ensure GitHub Discussions is enabled
- Verify Giscus app is installed
- Check `_config.yml` configuration
- Confirm `comments: true` in publication frontmatter

**"Duplicate publications created"**
- The script uses caching to prevent duplicates
- Delete `.orcid_cache.json` to force full refresh
- Check publication permalinks for conflicts

### Debug Mode
Enable detailed logging:
```python
# Change logging level in orcid_publications_manager.py
logging.basicConfig(level=logging.DEBUG)
```

### Cache Management
```bash
# Clear cache to force full refresh
rm .orcid_cache.json

# View cached data
cat .orcid_cache.json | python3 -m json.tool
```

## Migration from CSV Tool

The old `markdown_generator` tool used CSV files. This new tool:

1. **Replaces**: `publications.py` and CSV workflow
2. **Improves**: Automatic data fetching from authoritative source (ORCID)
3. **Adds**: Comments system and better caching
4. **Maintains**: Same Jekyll publication format for compatibility

To migrate:
1. Backup your current `_publications/` directory
2. Run the new ORCID manager
3. Compare results and adjust as needed
4. Remove old CSV files and scripts when satisfied

## Contributing

Found an issue or want to improve the script? Please:
1. Check existing GitHub issues
2. Create a detailed bug report or feature request
3. Submit pull requests with tests and documentation

## License

This tool is part of your Jekyll academic website and follows the same license terms.