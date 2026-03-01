#!/usr/bin/env python3
"""
Add Favicon to All Writeup HTML Files
Adds a favicon link tag to the <head> section of all HTML files
"""

import os
import re

def add_favicon_to_html(html_path, favicon_path="writeup.png"):
    """Add favicon link to HTML file if not already present"""
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"    ✗ Error reading {html_path}: {e}")
        return False
    
    # Check if favicon already exists
    if 'rel="icon"' in content or 'rel="shortcut icon"' in content or 'favicon' in content.lower():
        return False  # Already has a favicon
    
    # Create the favicon link tag
    favicon_tag = f'    <link rel="icon" type="image/png" href="{favicon_path}">\n'
    
    # Find the </head> tag and insert favicon before it
    if '</head>' in content:
        content = content.replace('</head>', f'{favicon_tag}</head>', 1)
    elif '<head>' in content:
        # If no </head>, add after <head>
        content = content.replace('<head>', f'<head>\n{favicon_tag}', 1)
    else:
        print(f"    ⚠ No <head> tag found in {html_path}")
        return False
    
    # Write back to file
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"    ✗ Error writing {html_path}: {e}")
        return False

def process_all_html_files():
    """Process all HTML files in the current directory and root"""
    
    print("🖼️  Adding Favicon to Writeup HTML Files")
    print("=" * 70)
    print(f"Favicon: writeup.png")
    print("=" * 70)
    
    # Find all HTML files in current directory (root)
    html_files = [f for f in os.listdir('.') 
                  if os.path.isfile(f) and (f.endswith('.html') or f.endswith('.htm')) 
                  and f.lower() != 'index.html']
    
    if not html_files:
        print("\n❌ No HTML files found in current directory")
        print("Make sure you're running this from your repository root!")
        return
    
    print(f"\n📄 Found {len(html_files)} HTML file(s)\n")
    
    total_updated = 0
    total_skipped = 0
    
    for html_file in sorted(html_files):
        print(f"  📄 {html_file}")
        
        if add_favicon_to_html(html_file):
            print(f"    ✓ Added favicon")
            total_updated += 1
        else:
            print(f"    ℹ Already has favicon (skipped)")
            total_skipped += 1
    
    print("\n" + "=" * 70)
    print(f"\n✓ SUMMARY:")
    print(f"  • Updated: {total_updated} file(s)")
    print(f"  • Skipped: {total_skipped} file(s) (already had favicon)")
    print(f"  • Total processed: {len(html_files)} file(s)")
    
    if total_updated > 0:
        print("\n📝 Next steps:")
        print("  1. Make sure 'writeup.png' is in your repository root")
        print("  2. Commit and push:")
        print("     git add .")
        print("     git commit -m 'Add favicon to writeup pages'")
        print("     git push")
    
    print("\n💡 Note: The favicon path is relative to each HTML file.")
    print("   Make sure writeup.png is in the same directory as your HTML files!")

if __name__ == "__main__":
    process_all_html_files()
