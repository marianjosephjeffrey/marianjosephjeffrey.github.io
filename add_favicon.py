#!/usr/bin/env python3
"""
Add Favicon to Writeup HTML Files
This script adds a shield emoji favicon to all HTML files in KC7 and TryHackMe folders
"""

import os
import sys

# Favicon code to add (shield emoji)
FAVICON = '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'%3E%3Ctext y=\'.9em\' font-size=\'90\'%3E🛡️%3C/text%3E%3C/svg%3E">'

def add_favicon_to_html(file_path):
    """Add favicon to HTML file if not present"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Error reading {file_path}: {e}")
        return False
    
    # Check if favicon already exists
    if 'rel="icon"' in content or 'favicon' in content.lower():
        print(f"✓ {file_path} already has favicon (skipped)")
        return False
    
    # Find the best insertion point
    modified = False
    
    # Try after </title>
    if '</title>' in content:
        content = content.replace('</title>', f'</title>\n    {FAVICON}', 1)
        modified = True
    # Try after <head>
    elif '<head>' in content.lower():
        # Case insensitive replacement
        import re
        pattern = re.compile(r'<head>', re.IGNORECASE)
        content = pattern.sub(f'<head>\n    {FAVICON}', content, count=1)
        modified = True
    else:
        print(f"✗ {file_path} - Could not find <head> or <title> tag")
        return False
    
    if not modified:
        return False
    
    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Added favicon to {file_path}")
        return True
    except Exception as e:
        print(f"✗ Error writing {file_path}: {e}")
        return False

def main():
    """Main function to process all HTML files"""
    folders = ['KC7', 'TryHackMe']
    total_processed = 0
    total_modified = 0
    
    print("🛡️  Adding Favicon to Writeup HTML Files")
    print("=" * 50)
    
    for folder in folders:
        if not os.path.exists(folder):
            print(f"\n📁 Folder '{folder}' not found (skipping)")
            continue
        
        print(f"\n📁 Processing folder: {folder}")
        print("-" * 50)
        
        files_in_folder = [f for f in os.listdir(folder) 
                          if f.endswith('.html') or f.endswith('.htm')]
        
        if not files_in_folder:
            print(f"   No HTML files found in {folder}")
            continue
        
        for filename in files_in_folder:
            file_path = os.path.join(folder, filename)
            total_processed += 1
            if add_favicon_to_html(file_path):
                total_modified += 1
    
    print("\n" + "=" * 50)
    print(f"✓ Done! Processed {total_processed} files, modified {total_modified} files.")
    
    if total_modified > 0:
        print("\n📝 Next steps:")
        print("   1. Review the changes")
        print("   2. git add .")
        print("   3. git commit -m 'Add favicon to writeups'")
        print("   4. git push")

if __name__ == "__main__":
    main()
