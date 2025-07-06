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

# Get system architecture
ARCH=$(uname -m)

# Check for gthread library and set parameter if found
GTHREAD_LIB=$(find /usr/lib* -name "libgthread-2.0.so.0" 2>/dev/null | head -1)
if [ -n "$GTHREAD_LIB" ]; then
	GTHREAD_PARAM="--include-data-files=$GTHREAD_LIB=./libgthread-2.0.so.0"
	echo "Found gthread library at: $GTHREAD_LIB"
else
	GTHREAD_PARAM=""
	echo "Warning: gthread library not found. The executable may require libgthread-2.0 to be installed on target systems."
fi

# Build with versioned output name
if [ -n "$ICON_PARAM" ]; then
	python -m nuitka start.py \
	--standalone \
	--onefile \
	--enable-plugin=pyside6 \
	--output-dir=dist \
	--output-filename="multiringstrobodiscgen-v${VERSION}-${ARCH}.bin" \
	--include-module=svgwrite \
	--include-module=svglib \
	--include-module=tempfile \
	--include-module=reportlab \
	--include-package=reportlab \
	--onefile-tempdir-spec="{TEMP}/multiringstrobodiscgen" \
	--assume-yes-for-downloads \
	$GTHREAD_PARAM \
	--windows-console-mode=disable \
	$ICON_PARAM
else
	python -m nuitka start.py \
	--standalone \
	--onefile \
	--enable-plugin=pyside6 \
	--output-dir=dist \
	--output-filename="multiringstrobodiscgen-v${VERSION}-${ARCH}.bin" \
	--include-module=svgwrite \
	--include-module=svglib \
	--include-module=tempfile \
	--include-module=reportlab \
	--include-package=reportlab \
	--onefile-tempdir-spec="{TEMP}/multiringstrobodiscgen" \
	--assume-yes-for-downloads \
	$GTHREAD_PARAM \
	--windows-console-mode=disable
fi

output_file="dist/multiringstrobodiscgen-v${VERSION}-${ARCH}.bin"
echo "The executable '${output_file}' has been created."