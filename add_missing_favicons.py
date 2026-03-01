#!/usr/bin/env python3
"""
Add Missing Favicons to HTML Files
Only updates files that don't have writeup.png favicon
"""

import os
import re

def needs_favicon(html_path):
    """Check if file needs favicon added"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Check if already has writeup.png
        return 'writeup.png' not in content
    except:
        return False

def add_favicon_to_html(html_path):
    """Add favicon to HTML file"""
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"    ✗ Error reading: {e}")
        return False
    
    # Favicon tags
    favicon_tag = '    <link rel="icon" type="image/png" href="writeup.png">\n'
    
    # Find best insertion point
    # Try after <meta charset>
    if re.search(r'<meta[^>]*charset[^>]*>', content, re.IGNORECASE):
        content = re.sub(
            r'(<meta[^>]*charset[^>]*>\s*)',
            r'\1' + favicon_tag,
            content,
            count=1,
            flags=re.IGNORECASE
        )
    # Try after <head>
    elif re.search(r'<head[^>]*>', content, re.IGNORECASE):
        content = re.sub(
            r'(<head[^>]*>\s*)',
            r'\1' + favicon_tag,
            content,
            count=1,
            flags=re.IGNORECASE
        )
    # Last resort - before </head>
    elif '</head>' in content:
        content = content.replace('</head>', favicon_tag + '</head>', 1)
    else:
        return False
    
    # Write back
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"    ✗ Error writing: {e}")
        return False

def main():
    print("🔧 Adding Missing Favicons")
    print("=" * 70)
    
    # Find HTML files that need favicons
    files_to_update = []
    
    for file in os.listdir('.'):
        if os.path.isfile(file) and (file.endswith('.html') or file.endswith('.htm')):
            if file.lower() != 'index.html' and needs_favicon(file):
                files_to_update.append(file)
    
    if not files_to_update:
        print("\n✓ All files already have favicons!")
        return
    
    print(f"\n📄 Found {len(files_to_update)} file(s) missing favicon\n")
    
    updated = 0
    failed = 0
    
    for html_file in sorted(files_to_update):
        print(f"  📄 {html_file}")
        if add_favicon_to_html(html_file):
            print(f"    ✓ Added favicon")
            updated += 1
        else:
            print(f"    ✗ Failed")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"\n✓ SUMMARY:")
    print(f"  • Added: {updated} favicon(s)")
    print(f"  • Failed: {failed}")
    
    if updated > 0:
        print("\n📝 Next:")
        print("  git add .")
        print("  git commit -m 'Add favicons to remaining writeups'")
        print("  git push")

if __name__ == "__main__":
    main()
