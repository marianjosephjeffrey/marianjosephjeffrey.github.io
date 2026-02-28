#!/usr/bin/env python3
"""
Fix Image Paths When Everything Is In Root
Structure: All HTML files and all image folders are in the root directory
Example: Anonforce.html and Anonforce/ folder both in root
"""

import os
import re

def fix_image_paths_everything_in_root(html_path):
    """Fix image paths when HTML and image folders are both in root"""
    
    html_filename = os.path.basename(html_path)
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"    ✗ Error reading: {e}")
        return False, 0
    
    original_content = content
    fixed_count = 0
    
    def fix_path(match):
        nonlocal fixed_count
        src_value = match.group(1)
        
        # Skip external URLs
        if src_value.startswith('http://') or src_value.startswith('https://'):
            return match.group(0)
        
        # Skip data URIs
        if src_value.startswith('data:'):
            return match.group(0)
        
        # Remove any TryHackMe/, KC7/, HackTheBox/ prefixes
        # Since everything is now in root, we don't need these
        cleaned_path = src_value
        cleaned_path = re.sub(r'^TryHackMe/', '', cleaned_path)
        cleaned_path = re.sub(r'^KC7/', '', cleaned_path)
        cleaned_path = re.sub(r'^HackTheBox/', '', cleaned_path)
        
        # Also remove triple prefixes if any
        cleaned_path = re.sub(r'^HackTheBox/HackTheBox/HackTheBox/', '', cleaned_path)
        
        if cleaned_path != src_value:
            fixed_count += 1
            return f'src="{cleaned_path}"'
        
        return match.group(0)
    
    # Fix all image src attributes
    content = re.sub(
        r'src="([^"]+\.(?:png|jpg|jpeg|gif|webp|svg|bmp|PNG|JPG|JPEG|GIF|WEBP|SVG|BMP))"',
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
    print("🔧 Fixing Image Paths - Everything In Root")
    print("=" * 70)
    print("Structure: HTML files and image folders are all in root directory")
    print("Example: Anonforce.html → Anonforce/image.png")
    print("=" * 70)
    
    # Find all HTML files in root directory
    html_files = [f for f in os.listdir('.') 
                  if os.path.isfile(f) and (f.endswith('.html') or f.endswith('.htm'))]
    
    if not html_files:
        print("\n❌ No HTML files found in current directory")
        print("\nMake sure you're running this from the repository root!")
        return
    
    print(f"\n📄 Found {len(html_files)} HTML file(s) in root directory\n")
    
    total_fixed = 0
    total_files = 0
    
    for html_file in html_files:
        # Skip index.html
        if html_file.lower() == 'index.html':
            continue
        
        print(f"  📄 {html_file}")
        
        changed, count = fix_image_paths_everything_in_root(html_file)
        
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
        print("\n📝 What was fixed:")
        print("  • Removed TryHackMe/ prefixes")
        print("  • Removed KC7/ prefixes")
        print("  • Removed HackTheBox/ prefixes")
        print("  • Now paths are relative to root (e.g., Anonforce/image.png)")
        
        print("\n📝 Next steps:")
        print("  1. Test a writeup to see if images load")
        print("  2. Commit and push:")
        print("     git add .")
        print("     git commit -m 'Fix image paths for root structure'")
        print("     git push")
    else:
        print("\n  ✅ All paths already correct!")
        print("\n  If images still don't load, try running:")
        print("     python diagnose_images.py")

if __name__ == "__main__":
    main()
