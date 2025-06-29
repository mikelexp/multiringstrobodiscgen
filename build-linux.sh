#!/bin/bash
# This script compiles the Python script into a standalone executable using Nuitka.

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
	echo "Error: The 'venv' directory does not exist. Please set up the virtual environment first."
	exit 1
fi

source venv/bin/activate

# Check if icon file exists
if [ ! -f "gfx/icon.png" ]; then
	echo "Warning: 'gfx/icon.png' not found. The executable will be created without an embedded icon."
	ICON_PARAM=""
else
	ICON_PARAM="--linux-icon=gfx/icon.png"
fi

# Get version from version.py
VERSION=$(python src/version.py)

# Build with versioned output name
if [ -n "$ICON_PARAM" ]; then
	python -m nuitka start.py \
	--standalone \
	--onefile \
	--enable-plugin=pyside6 \
	--output-dir=dist \
	--output-filename="multiringstrobodiscgen-v${VERSION}.bin" \
	--include-module=svgwrite \
	--include-module=svglib \
	--include-module=tempfile \
	--include-module=reportlab \
	--include-package=reportlab \
	--windows-console-mode=disable \
	$ICON_PARAM
else
	python -m nuitka start.py \
	--standalone \
	--onefile \
	--enable-plugin=pyside6 \
	--output-dir=dist \
	--output-filename="multiringstrobodiscgen-v${VERSION}.bin" \
	--include-module=svgwrite \
	--include-module=svglib \
	--include-module=tempfile \
	--include-module=reportlab \
	--include-package=reportlab \
	--windows-console-mode=disable
fi

# Create a symlink for packages to use
cd dist
ln -sf "multiringstrobodiscgen-v${VERSION}.bin" "multiringstrobodiscgen.bin"
cd ..

output_file="dist/multiringstrobodiscgen-v${VERSION}.bin"
echo "The executable '${output_file}' has been created."
echo "Symlink created at 'dist/multiringstrobodiscgen.bin' for package builds."