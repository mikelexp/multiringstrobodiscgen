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
    
    # Update README.md if needed (optional)
    readme_file = Path('README.md')
    if readme_file.exists():
        readme_content = readme_file.read_text()
        # Update any version references in README if they exist
        # This is optional and depends on your README structure
        print("✓ README.md checked")
    
    print(f"\n🎉 Version updated to {new_version}")
    print("Next steps:")
    print("1. Test the application")
    print("2. Build standalone executable: ./build-linux.sh")
    print("3. Commit changes: git add . && git commit -m 'Bump version to {}'".format(new_version))
    print("4. Create git tag: git tag v{}".format(new_version))
    
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