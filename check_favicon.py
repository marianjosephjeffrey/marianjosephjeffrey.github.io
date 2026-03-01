#!/usr/bin/env python3
"""
Check Favicon Status in HTML Files
Diagnose whether favicons are properly set
"""

import os
import re

def check_favicon_in_html(html_path):
    """Check if HTML file has a favicon"""
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"ERROR: {e}"
    
    # Look for favicon links
    favicon_matches = re.findall(r'<link[^>]*rel=["\'](?:icon|shortcut icon)[^>]*>', content, re.IGNORECASE)
    
    if not favicon_matches:
        return "❌ NO FAVICON"
    
    # Show what was found
    results = []
    for match in favicon_matches:
        # Extract href
        href_match = re.search(r'href=["\']([^"\']+)["\']', match)
        if href_match:
            results.append(f"✓ {href_match.group(1)}")
    
    return " | ".join(results) if results else "⚠ Found tag but no href"

def main():
    print("🔍 Checking Favicon Status in HTML Files")
    print("=" * 70)
    
    # Find all HTML files
    html_files = []
    for file in os.listdir('.'):
        if os.path.isfile(file) and (file.endswith('.html') or file.endswith('.htm')):
            html_files.append(file)
    
    if not html_files:
        print("\n❌ No HTML files found")
        return
    
    print(f"\n📄 Checking {len(html_files)} file(s)\n")
    
    has_favicon = 0
    no_favicon = 0
    
    for html_file in sorted(html_files):
        status = check_favicon_in_html(html_file)
        print(f"  {html_file}")
        print(f"    {status}")
        
        if "✓" in status:
            has_favicon += 1
        elif "❌" in status:
            no_favicon += 1
    
    print("\n" + "=" * 70)
    print(f"\n📊 SUMMARY:")
    print(f"  • Has favicon: {has_favicon}")
    print(f"  • Missing favicon: {no_favicon}")
    print(f"  • Total: {len(html_files)}")
    
    if no_favicon > 0:
        print(f"\n💡 Run 'python add_favicon_improved.py' to add favicons")

if __name__ == "__main__":
    main()
