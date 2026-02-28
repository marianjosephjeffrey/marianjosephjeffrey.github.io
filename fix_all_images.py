#!/usr/bin/env python3
"""
Fix ALL Image Path Issues in HTML Files
Handles multiple path formats and ensures images load correctly
"""

import os
import re
from urllib.parse import unquote

def fix_all_image_paths(html_path, folder_name):
    """Fix all types of broken image paths"""
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"    ✗ Error reading: {e}")
        return False, 0
    
    original_content = content
    fixed_count = 0
    
    # Pattern 1: Fix src="SubfolderName/image.png" -> src="TryHackMe/SubfolderName/image.png"
    def fix_missing_folder(match):
        nonlocal fixed_count
        src_value = match.group(1)
        
        # Skip if already correct
        if src_value.startswith(f'{folder_name}/'):
            return match.group(0)
        if src_value.startswith('http://') or src_value.startswith('https://'):
            return match.group(0)
        if src_value.startswith('data:'):
            return match.group(0)
        
        # Has a subfolder structure that needs folder prefix
        if '/' in src_value:
            fixed_count += 1
            return f'src="{folder_name}/{src_value}"'
        
        return match.group(0)
    
    # Fix paths
    content = re.sub(
        r'src="([^"]+\.(?:png|jpg|jpeg|gif|webp|svg|bmp|PNG|JPG|JPEG|GIF|WEBP|SVG|BMP))"',
        fix_missing_folder,
        content
    )
    
    # Pattern 2: Decode URL encoding (%20 -> space, etc.)
    content = re.sub(
        r'src="([^"]*%[0-9A-Fa-f]{2}[^"]*)"',
        lambda m: f'src="{unquote(m.group(1))}"',
        content
    )
    
    # Pattern 3: Remove file:// URLs completely and replace with relative path
    def fix_file_urls(match):
        nonlocal fixed_count
        file_url = match.group(1)
        
        # Extract just the filename or relative path from file URL
        # file:///Users/.../TryHackMe/SubFolder/image.png -> TryHackMe/SubFolder/image.png
        
        # Decode URL encoding
        decoded = unquote(file_url)
        
        # Try to extract the folder name and everything after it
        if f'/{folder_name}/' in decoded:
            # Extract from folder name onwards
            parts = decoded.split(f'/{folder_name}/')
            if len(parts) >= 2:
                fixed_count += 1
                return f'src="{folder_name}/{parts[-1]}"'
        
        # Fallback: just get filename
        filename = decoded.split('/')[-1]
        if filename:
            fixed_count += 1
            return f'src="{filename}"'
        
        return match.group(0)
    
    content = re.sub(
        r'src="file:///([^"]+)"',
        fix_file_urls,
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

def verify_images_exist(folder):
    """Check which images actually exist in the folder"""
    
    image_files = set()
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp')):
                # Get relative path from folder
                rel_path = os.path.relpath(os.path.join(root, file), folder)
                image_files.add(rel_path)
    
    return image_files

def main():
    print("🖼️  Comprehensive Image Path Fixer")
    print("=" * 70)
    
    folders = ['TryHackMe', 'KC7', 'HackTheBox']
    total_fixed = 0
    total_files = 0
    
    for folder in folders:
        if not os.path.exists(folder):
            print(f"\n📁 '{folder}/' not found (skipping)")
            continue
        
        print(f"\n📁 Processing {folder}/")
        print("-" * 70)
        
        # Check what images exist
        existing_images = verify_images_exist(folder)
        print(f"  Found {len(existing_images)} image file(s) in folder")
        
        # Find all HTML files (including in subfolders)
        html_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.html') or file.endswith('.htm'):
                    html_path = os.path.join(root, file)
                    rel_path = os.path.relpath(html_path, folder)
                    html_files.append((rel_path, html_path))
        
        if not html_files:
            print(f"  No HTML files found")
            continue
        
        print(f"  Found {len(html_files)} HTML file(s)\n")
        
        for rel_name, html_path in html_files:
            print(f"  📄 {rel_name}")
            
            changed, count = fix_all_image_paths(html_path, folder)
            
            if changed:
                print(f"    ✓ Fixed {count} path(s)")
                total_fixed += count
                total_files += 1
            else:
                print(f"    ℹ No changes needed")
    
    print("\n" + "=" * 70)
    print(f"\n✓ SUMMARY:")
    print(f"  • Modified: {total_files} file(s)")
    print(f"  • Fixed: {total_fixed} image path(s)")
    
    if total_fixed > 0:
        print("\n📝 Next steps:")
        print("  1. Test a writeup locally")
        print("  2. If images still don't load, check browser console for exact errors")
        print("  3. Commit and push:")
        print("     git add .")
        print("     git commit -m 'Fix all image paths'")
        print("     git push")
        print("\n💡 Tip: If images STILL don't show, the issue might be:")
        print("  - Image files are in wrong folders")
        print("  - Image filenames don't match (case sensitive)")
        print("  - Need to run fix_paths_final.py first")

if __name__ == "__main__":
    main()
