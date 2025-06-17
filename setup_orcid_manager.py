#!/usr/bin/env python3
"""
Setup script for ORCID Publications Manager

This script sets up the environment and provides instructions for using the ORCID manager.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ['requests', 'yaml']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    return missing

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    
    try:
        # Try installing with --user flag first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "requests", "PyYAML"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies automatically.")
        print("\nPlease install manually:")
        print("pip3 install --user requests PyYAML")
        print("or")
        print("pip3 install --break-system-packages requests PyYAML")
        return False

def setup_giscus():
    """Provide instructions for setting up Giscus comments"""
    print("\n🔧 GISCUS COMMENTS SETUP INSTRUCTIONS")
    print("=" * 50)
    print("To enable comments on your publication pages, follow these steps:")
    print()
    print("1. Enable GitHub Discussions on your repository:")
    print("   - Go to https://github.com/hydrotian/hydrotian.github.io/settings")
    print("   - Scroll down to 'Features' section")
    print("   - Check 'Discussions' to enable it")
    print()
    print("2. Install the Giscus app:")
    print("   - Visit https://github.com/apps/giscus")
    print("   - Click 'Install' and select your repository")
    print()
    print("3. Get your Giscus configuration:")
    print("   - Visit https://giscus.app/")
    print("   - Enter your repository: hydrotian/hydrotian.github.io")
    print("   - Choose 'Discussions' mapping")
    print("   - Select or create a 'Comments' category")
    print("   - Copy the data-repo-id and data-category-id values")
    print()
    print("4. Update your _config.yml with the values:")
    print("   giscus:")
    print("     repo_id: \"[YOUR_REPO_ID]\"")
    print("     category_id: \"[YOUR_CATEGORY_ID]\"")
    print()

def main():
    """Main setup function"""
    print("🚀 ORCID Publications Manager Setup")
    print("=" * 40)
    
    # Check current directory
    if not Path("_config.yml").exists():
        print("❌ Error: This script must be run from your Jekyll site root directory")
        print("Please navigate to your Jekyll site directory and run again.")
        return
    
    print("✅ Jekyll site detected")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        if not install_dependencies():
            return
    else:
        print("✅ All dependencies available")
    
    # Setup instructions
    setup_giscus()
    
    print("\n📋 USAGE INSTRUCTIONS")
    print("=" * 25)
    print("1. Complete the Giscus setup above")
    print("2. Run the ORCID manager:")
    print("   python3 orcid_publications_manager.py")
    print()
    print("3. The script will:")
    print("   - Fetch your publications from ORCID")
    print("   - Create Jekyll pages for new publications")
    print("   - Enable comments on each publication")
    print("   - Generate placeholder images")
    print()
    print("4. After running, commit and push your changes:")
    print("   git add .")
    print("   git commit -m 'Update publications from ORCID'")
    print("   git push")
    print()
    print("🎉 Setup complete! Your ORCID manager is ready to use.")

if __name__ == "__main__":
    main()