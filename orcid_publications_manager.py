#!/usr/bin/env python3
"""
ORCID Publications Manager for Jekyll Academic Website

This script fetches publications from ORCID, compares with existing Jekyll publications,
and generates new publication pages automatically.

Author: Tian Zhou
ORCID: 0000-0003-1582-4005
"""

import requests
import json
import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional
import hashlib
import logging

# Configuration
ORCID_ID = "0000-0003-1582-4005"
ORCID_API_BASE = "https://pub.orcid.org/v3.0"
PUBLICATIONS_DIR = "_publications"
IMAGES_DIR = "images/papers"
CACHE_FILE = ".orcid_cache.json"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ORCIDPublicationManager:
    def __init__(self, orcid_id: str):
        self.orcid_id = orcid_id
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
        
        # Extract citation
        citation = ""
        if work_detail.get('citation') and work_detail['citation'].get('citation-value'):
            citation = work_detail['citation']['citation-value']
        
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
        
        # Simple description generation (can be enhanced with LLM API later)
        if 'model' in title.lower() or 'simulation' in title.lower():
            desc_type = "modeling study"
        elif 'analysis' in title.lower() or 'evaluation' in title.lower():
            desc_type = "research analysis"
        elif 'review' in title.lower():
            desc_type = "review paper"
        else:
            desc_type = "research paper"
        
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
        
        # Create publications directory if it doesn't exist
        pub_dir = Path(PUBLICATIONS_DIR)
        pub_dir.mkdir(exist_ok=True)
        
        # Generate filename
        filename = f"{pub_info['permalink']}.md"
        filepath = pub_dir / filename
        
        # Skip if file already exists
        if filepath.exists():
            logging.info(f"Publication already exists: {filename}")
            return
        
        # Generate description
        description = self.generate_publication_description(pub_info)
        
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
            if not pub_info.get('title'):
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
    manager = ORCIDPublicationManager(ORCID_ID)
    manager.sync_publications()


if __name__ == "__main__":
    main()