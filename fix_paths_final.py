#!/usr/bin/env python3
"""
Fix Image Paths - Add TryHackMe/KC7 Prefix
Based on actual Notion export format
"""

import os
import re

def fix_image_paths_in_html(html_path, folder_name):
    """Add folder prefix to image paths that need it"""
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"    ✗ Error reading: {e}")
        return False, 0
    
    original_content = content
    fixed_count = 0
    
    # Pattern to match image sources that need fixing
    # Matches: src="SomeFolderName/image.png"
    # But NOT: src="TryHackMe/..." or src="KC7/..." or src="http..."
    
    def fix_path(match):
        nonlocal fixed_count
        src_value = match.group(1)
        
        # Skip if already has TryHackMe/ or KC7/ prefix
        if src_value.startswith('TryHackMe/') or src_value.startswith('KC7/'):
            return match.group(0)
        
        # Skip external URLs
        if src_value.startswith('http://') or src_value.startswith('https://'):
            return match.group(0)
        
        # Skip if it's just a filename with no slash (shouldn't happen but just in case)
        if '/' not in src_value:
            return match.group(0)
        
        # This is a path that needs the folder prefix
        # e.g., "AI%20in%20Security/image.png" -> "TryHackMe/AI%20in%20Security/image.png"
        fixed_count += 1
        return f'src="{folder_name}/{src_value}"'
    
    # Replace all src=".../.../image.ext" that don't start with http or folder name
    content = re.sub(
        r'src="([^"]+/[^"]+\.(?:png|jpg|jpeg|gif|webp|svg|bmp|PNG|JPG|JPEG|GIF|WEBP|SVG|BMP))"',
        fix_path,
        content
    )
    
    if content != original_content:
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, fixed_count
        except Exception as e:
            print(f"    ✗ Error writing: {e}")
            return False, 0
    
    return False, 0

def main():
    print("🔧 Adding Folder Prefix to Image Paths")
    print("=" * 70)
    
    folders = ['TryHackMe', 'KC7']
    total_fixed = 0
    total_files = 0
    
    for folder in folders:
        if not os.path.exists(folder):
            print(f"\n📁 '{folder}/' not found (skipping)")
            continue
        
        print(f"\n📁 Processing {folder}/")
        print("-" * 70)
        
        # Find all HTML files
        html_files = []
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            if os.path.isfile(item_path) and item.endswith('.html'):
                html_files.append(item)
        
        if not html_files:
            print(f"  No HTML files found")
            continue
        
        print(f"  Found {len(html_files)} HTML file(s)\n")
        
        for html_file in html_files:
            html_path = os.path.join(folder, html_file)
            print(f"  📄 {html_file}")
            
            changed, count = fix_image_paths_in_html(html_path, folder)
            
            if changed:
                print(f"    ✓ Fixed {count} path(s)")
                total_fixed += count
                total_files += 1
            else:
                print(f"    ℹ Already correct")
    
    print("\n" + "=" * 70)
    print(f"\n✓ SUMMARY:")
    print(f"  • Modified: {total_files} file(s)")
    print(f"  • Fixed: {total_fixed} image path(s)")
    
    if total_fixed > 0:
        print("\n📝 Next:")
        print("  git add .")
        print("  git commit -m 'Fix image folder paths'")
        print("  git push")
    else:
        print("\nℹ️  No changes needed - paths already correct!")

if __name__ == "__main__":
    main()
