#!/usr/bin/env python3
"""
ORCID Publications Manager for Jekyll Academic Website

This script fetches publications from ORCID, compares with existing Jekyll publications,
and generates new publication pages automatically.

Author: Tian Zhou
ORCID: 0000-0003-1582-4005
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional
import logging

try:
    import requests
    import yaml
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Please install with: pip install requests PyYAML")
    exit(1)

# Configuration
ORCID_ID = "0000-0003-1582-4005"
ORCID_API_BASE = "https://pub.orcid.org/v3.0"
PUBLICATIONS_DIR = "_publications"
IMAGES_DIR = "images/papers"
CACHE_FILE = ".orcid_cache.json"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ORCIDPublicationManager:
    def __init__(self, orcid_id: str, min_year: int = 2024, dry_run: bool = False):
        self.orcid_id = orcid_id
        self.min_year = min_year
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.orcid+json',
            'User-Agent': 'ORCID-Jekyll-Publication-Manager/1.0'
        })
        
    def fetch_works_summary(self) -> List[Dict]:
        """Fetch summary of all works from ORCID"""
        url = f"{ORCID_API_BASE}/{self.orcid_id}/works"
        logging.info(f"Fetching works from: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            works = data.get('group', [])
            logging.info(f"Found {len(works)} work groups")
            return works
        except requests.RequestException as e:
            logging.error(f"Failed to fetch works summary: {e}")
            return []
    
    def fetch_work_details(self, put_code: str) -> Optional[Dict]:
        """Fetch detailed information for a specific work"""
        url = f"{ORCID_API_BASE}/{self.orcid_id}/work/{put_code}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch work details for {put_code}: {e}")
            return None
    
    def generate_agu_citation(self, work_detail: Dict, title: str, venue: str, pub_date: str, doi: str) -> str:
        """Generate simple AGU-style citation"""
        try:
            # Extract authors from contributors
            authors = []
            if work_detail.get('contributors') and work_detail['contributors'].get('contributor'):
                for contributor in work_detail['contributors']['contributor']:
                    if contributor.get('credit-name') and contributor['credit-name'].get('value'):
                        name = contributor['credit-name']['value']
                        # Convert to Last, F. M. format
                        authors.append(self.format_author_name(name))
            
            # If no contributors, try to extract from any citation
            if not authors and work_detail.get('citation'):
                authors = self.extract_authors_from_citation(work_detail['citation'].get('citation-value', ''))
            
            # Build AGU-style citation: Authors (Year), Title, Journal, doi
            parts = []
            
            # Authors
            if authors:
                if len(authors) == 1:
                    author_str = authors[0]
                elif len(authors) == 2:
                    author_str = f"{authors[0]} and {authors[1]}"
                elif len(authors) <= 5:
                    author_str = ", ".join(authors[:-1]) + f", and {authors[-1]}"
                else:
                    author_str = f"{authors[0]} et al."
                parts.append(author_str)
            
            # Year
            year = pub_date[:4] if pub_date else ""
            if year:
                parts.append(f"({year})")
            
            # Title (no quotes for AGU style)
            if title:
                parts.append(title)
            
            # Journal
            if venue:
                parts.append(venue)
            
            # DOI
            if doi:
                parts.append(f"https://doi.org/{doi}")
            
            return ", ".join(parts) + "."
            
        except Exception as e:
            logging.warning(f"Failed to generate AGU citation: {e}")
            return f"{title} ({pub_date[:4] if pub_date else 'n.d.'}), {venue}."
    
    def format_author_name(self, full_name: str) -> str:
        """Convert full name to Last, F. M. format"""
        try:
            parts = full_name.strip().split()
            if len(parts) < 2:
                return full_name
            
            # Last name is typically the last part
            last_name = parts[-1]
            first_names = parts[:-1]
            
            # Create initials
            initials = []
            for name in first_names:
                if name and len(name) > 0:
                    initials.append(f"{name[0]}.")
            
            return f"{last_name}, {' '.join(initials)}"
        except:
            return full_name
    
    def extract_authors_from_citation(self, citation: str) -> list:
        """Extract author names from citation string"""
        try:
            if citation.startswith('@'):
                # BibTeX format
                author_match = re.search(r'author\s*=\s*\{([^}]+)\}', citation)
                if author_match:
                    authors_str = author_match.group(1)
                    # Split by 'and' and clean up
                    authors = [a.strip() for a in re.split(r'\s+and\s+', authors_str)]
                    return [self.format_author_name(a) for a in authors[:5]]  # Max 5 authors
            return []
        except:
            return []

    def extract_publication_info(self, work_detail: Dict) -> Dict:
        """Extract relevant publication information from ORCID work detail"""
        if not work_detail:
            return {}
            
        # Extract basic information
        title = ""
        if work_detail.get('title') and work_detail['title'].get('title'):
            title = work_detail['title']['title']['value']

        # Extract journal/venue
        venue = ""
        if work_detail.get('journal-title') and work_detail['journal-title'].get('value'):
            venue = work_detail['journal-title']['value']
        
        # Extract publication date
        pub_date = None
        if work_detail.get('publication-date'):
            date_info = work_detail['publication-date']
            year = date_info.get('year', {}).get('value') if date_info.get('year') else None
            month = date_info.get('month', {}).get('value', '01') if date_info.get('month') else '01'
            day = date_info.get('day', {}).get('value', '01') if date_info.get('day') else '01'
            if year:
                pub_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # Extract DOI and URL
        doi = ""
        paper_url = ""
        if work_detail.get('external-ids') and work_detail['external-ids'].get('external-id'):
            for ext_id in work_detail['external-ids']['external-id']:
                if ext_id.get('external-id-type') == 'doi':
                    doi = ext_id.get('external-id-value', '')
                    if doi and not paper_url:
                        paper_url = f"https://doi.org/{doi}"
                elif ext_id.get('external-id-type') == 'url':
                    if not paper_url:
                        paper_url = ext_id.get('external-id-value', '')
        
        # Generate simple AGU-style citation
        citation = self.generate_agu_citation(work_detail, title, venue, pub_date, doi)
        
        # Create filename-safe permalink
        year = pub_date[:4] if pub_date else "unknown"
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]  # Limit length
        permalink = f"{year}-{safe_title}" if safe_title else f"{year}-publication"
        
        return {
            'title': title,
            'venue': venue,
            'date': pub_date,
            'doi': doi,
            'paper_url': paper_url,
            'citation': citation,
            'permalink': permalink,
            'put_code': work_detail.get('put-code'),
            'work_type': work_detail.get('type', 'journal-article')
        }
    
    def get_existing_publications(self) -> Set[str]:
        """Get list of existing publication permalinks"""
        existing = set()
        pub_dir = Path(PUBLICATIONS_DIR)
        
        if pub_dir.exists():
            for md_file in pub_dir.glob("*.md"):
                # Extract permalink from filename (remove .md extension)
                permalink = md_file.stem
                existing.add(permalink)
        
        return existing
    
    def load_cache(self) -> Dict:
        """Load cached ORCID data"""
        cache_path = Path(CACHE_FILE)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                logging.warning("Failed to load cache, starting fresh")
        return {'publications': {}, 'last_updated': None}
    
    def save_cache(self, data: Dict):
        """Save ORCID data to cache"""
        data['last_updated'] = datetime.now().isoformat()
        try:
            with open(CACHE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            logging.error(f"Failed to save cache: {e}")
    
    def generate_publication_description(self, pub_info: Dict) -> str:
        """Generate a brief description using the title and venue"""
        title = pub_info.get('title', '')
        venue = pub_info.get('venue', '')
        is_preprint = pub_info.get('work_type') == 'preprint'

        # Simple description generation (can be enhanced with LLM API later)
        if 'model' in title.lower() or 'simulation' in title.lower():
            desc_type = "modeling study"
        elif 'analysis' in title.lower() or 'evaluation' in title.lower():
            desc_type = "research analysis"
        elif 'review' in title.lower():
            desc_type = "review paper"
        else:
            desc_type = "research paper"

        if is_preprint:
            description = f"This {desc_type} preprint posted on {venue}" if venue else f"This {desc_type} preprint"
        else:
            description = f"This {desc_type} published in {venue}" if venue else f"This {desc_type}"
        
        # Add topic-specific context based on common keywords
        if any(word in title.lower() for word in ['water', 'hydro', 'climate', 'precipitation']):
            description += " focuses on water resources and climate modeling."
        elif any(word in title.lower() for word in ['model', 'simulation', 'numerical']):
            description += " presents computational modeling and simulation results."
        else:
            description += " contributes to our understanding of Earth system processes."
        
        return description
    
    def create_jekyll_publication(self, pub_info: Dict):
        """Create Jekyll publication markdown file"""
        if not pub_info.get('title'):
            logging.warning("Skipping publication without title")
            return

        # Skip supplementary-material companion entries from preprint servers
        if pub_info['title'].lower().startswith('supplementary material to'):
            logging.info(f"Skipping supplementary-material entry: {pub_info['title'][:80]}")
            return

        # Generate filename
        filename = f"{pub_info['permalink']}.md"
        
        # Simple year filter - extract year from filename
        year_match = re.match(r'^(\d{4})-', filename)
        if year_match:
            file_year = int(year_match.group(1))
            if file_year < self.min_year:
                if self.dry_run:
                    logging.info(f"[DRY RUN] Skipping {filename} (year {file_year} < {self.min_year})")
                else:
                    logging.info(f"Skipping {filename} (year {file_year} < {self.min_year})")
                return
        
        if self.dry_run:
            logging.info(f"[DRY RUN] Would create: {filename}")
            return
        
        # Create publications directory if it doesn't exist
        pub_dir = Path(PUBLICATIONS_DIR)
        pub_dir.mkdir(exist_ok=True)
        
        filepath = pub_dir / filename
        
        # Skip if file already exists
        if filepath.exists():
            logging.info(f"Publication already exists: {filename}")
            return
        
        # Generate description
        description = self.generate_publication_description(pub_info)
        
        # Map ORCID work-type to a simple category used by the publications page
        work_type = pub_info.get('work_type', 'journal-article')
        pubtype = 'preprint' if work_type == 'preprint' else 'journal-article'

        # Create frontmatter
        frontmatter = {
            'title': pub_info['title'],
            'collection': 'publications',
            'permalink': f"/publication/{pub_info['permalink']}",
            'excerpt': description,
            'date': pub_info.get('date', datetime.now().strftime('%Y-%m-%d')),
            'venue': pub_info.get('venue', ''),
            'paperurl': pub_info.get('paper_url', ''),
            'citation': pub_info.get('citation', ''),
            'pubtype': pubtype,
            'comments': True  # Enable comments on publication pages
        }
        
        # Create content
        content = f"---\n{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)}---\n"
        content += f"{description}\n\n"
        
        if pub_info.get('paper_url'):
            content += f"[Link to the paper]({pub_info['paper_url']})\n\n"
        
        # Add placeholder for image
        image_filename = f"{pub_info['permalink']}.png"
        content += f"<!-- Add publication image below -->\n"
        content += f"<!-- ![image](/{IMAGES_DIR}/{image_filename}) -->\n\n"
        
        if pub_info.get('citation'):
            content += f"Recommended citation: {pub_info['citation']}"
        
        # Write file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Created new publication: {filename}")
        except IOError as e:
            logging.error(f"Failed to create publication file {filename}: {e}")
    
    def sync_publications(self):
        """Main method to sync publications from ORCID"""
        logging.info("Starting ORCID publication sync...")
        
        # Load cache
        cache = self.load_cache()
        cached_pubs = cache.get('publications', {})
        
        # Fetch current works from ORCID
        works_summary = self.fetch_works_summary()
        if not works_summary:
            logging.error("No works found or failed to fetch from ORCID")
            return
        
        # Get existing publications
        existing_pubs = self.get_existing_publications()
        
        new_publications = []
        current_put_codes = set()
        
        # Process each work group
        for group in works_summary:
            work_summaries = group.get('work-summary', [])
            if not work_summaries:
                continue
                
            # Get the most recent version (first one in the list)
            work_summary = work_summaries[0]
            put_code = str(work_summary.get('put-code'))
            current_put_codes.add(put_code)
            
            # Check if we already have this work cached
            if put_code in cached_pubs:
                pub_info = cached_pubs[put_code]
                if pub_info.get('permalink') not in existing_pubs:
                    # We have the data but file doesn't exist, recreate
                    self.create_jekyll_publication(pub_info)
                continue
            
            # Fetch detailed information
            work_detail = self.fetch_work_details(put_code)
            if not work_detail:
                continue
            
            # Extract publication information
            pub_info = self.extract_publication_info(work_detail)
            if not pub_info or not pub_info.get('title'):
                # Skip if filtered out by year or missing title
                continue
            
            # Cache the publication info
            cached_pubs[put_code] = pub_info
            
            # Create Jekyll file if it doesn't exist
            if pub_info.get('permalink') not in existing_pubs:
                self.create_jekyll_publication(pub_info)
                new_publications.append(pub_info['title'])
        
        # Clean up removed publications from cache
        removed_codes = set(cached_pubs.keys()) - current_put_codes
        for code in removed_codes:
            del cached_pubs[code]
            logging.info(f"Removed publication from cache: {code}")
        
        # Update cache
        cache['publications'] = cached_pubs
        self.save_cache(cache)
        
        # Summary
        logging.info(f"Sync complete. Found {len(current_put_codes)} total publications.")
        logging.info(f"Created {len(new_publications)} new publications.")
        
        if new_publications:
            logging.info("New publications created:")
            for title in new_publications:
                logging.info(f"  - {title}")


def main():
    """Main entry point"""
    import sys
    
    # Parse arguments
    min_year = 2024  # Default to 2024+
    dry_run = False
    
    for arg in sys.argv[1:]:
        if arg == "--dry-run":
            dry_run = True
        elif arg.isdigit():
            min_year = int(arg)
        elif arg == "--help":
            print("Usage: python orcid_publications_manager.py [YEAR] [--dry-run]")
            print("  YEAR: Minimum year to process (default: 2024)")
            print("  --dry-run: Show what would be created without actually creating files")
            return
    
    if dry_run:
        print(f"[DRY RUN] Would process publications from {min_year} onwards...")
    else:
        print(f"Processing publications from {min_year} onwards...")
    
    manager = ORCIDPublicationManager(ORCID_ID, min_year=min_year, dry_run=dry_run)
    manager.sync_publications()


if __name__ == "__main__":
    main()