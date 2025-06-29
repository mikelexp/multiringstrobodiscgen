#!/usr/bin/env python3
"""
Version update utility for MultiRing Strobo Disc Generator
Updates version in all relevant files
"""

import sys
import re
from pathlib import Path

def update_version(new_version):
    """Update version in version.py and related files"""
    
    # Validate version format (semantic versioning)
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print(f"Error: Invalid version format '{new_version}'. Use semantic versioning (e.g., 1.0.0)")
        return False
    
    # Parse version components
    major, minor, patch = map(int, new_version.split('.'))
    
    # Update version.py
    version_file = Path('src/version.py')
    if not version_file.exists():
        print("Error: version.py not found")
        return False
    
    content = version_file.read_text()
    
    # Update version string and tuple
    content = re.sub(r'__version__ = ".*"', f'__version__ = "{new_version}"', content)
    content = re.sub(r'__version_info__ = \(.*\)', f'__version_info__ = ({major}, {minor}, {patch})', content)
    
    version_file.write_text(content)
    print(f"✓ Updated version.py to {new_version}")
    
    # Update installforge_project.ifp
    ifp_file = Path('installforge_project.ifp')
    if ifp_file.exists():
        ifp_content = ifp_file.read_text(encoding='utf-8')
        ifp_content = re.sub(r'Program version = .*', f'Program version = {new_version}', ifp_content)
        ifp_file.write_text(ifp_content, encoding='utf-8', newline='\r\n')
        print(f"✓ Updated installforge_project.ifp to {new_version}")
    
    print(f"\n🎉 Version updated to {new_version}")
    print("Next steps:")
    print("1. Test the application: ./run.sh (Linux) or python3 start.py (Windows)")
    print("2. Build standalone executable: ./build-linux.sh (Linux) or build-windows.ps1 (Windows)")
    print("3. Commit changes: git add . && git commit -m 'Bump version to {}'".format(new_version))
    print("4. Create git tag: git tag v{}".format(new_version))
    print("5. Push new tag: git push --tags")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        print("Example: python update_version.py 1.0.1")
        sys.exit(1)
    
    new_version = sys.argv[1]
    if update_version(new_version):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()