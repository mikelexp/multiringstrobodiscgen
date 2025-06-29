# This script compiles the Python script into a standalone executable using Nuitka in Windows PowerShell.

# Check if the virtual environment directory exists
if (-Not (Test-Path "venv")) {
    Write-Error "Error: The 'venv' directory does not exist. Please set up the virtual environment first."
    exit 1
}

# Check if icon file exists
if (-Not (Test-Path "gfx\icon.ico")) {
    Write-Warning "Warning: 'gfx\icon.ico' not found. The executable will be created without an embedded icon."
    $ICON_PARAM = ""
} else {
    $ICON_PARAM = "--windows-icon-from-ico=gfx\icon.ico"
}

# Activate the virtual environment
& "venv\Scripts\Activate.ps1"

# Get version from version.py
$VERSION = python src/version.py

# Get system architecture
$ARCH = $Env:PROCESSOR_ARCHITECTURE

# Run Nuitka to compile the script with versioned name
if ($ICON_PARAM) {
    python -m nuitka start.py `
        --standalone `
        --onefile `
        --enable-plugin=pyside6 `
        --output-dir=dist `
        --output-filename="multiringstrobodiscgen-v$VERSION-$ARCH.exe" `
        --include-module=svgwrite `
        --include-module=svglib `
        --include-module=tempfile `
        --include-module=reportlab `
        --include-package=reportlab `
        --windows-console-mode=disable `
        $ICON_PARAM
} else {
    python -m nuitka start.py `
        --standalone `
        --onefile `
        --enable-plugin=pyside6 `
        --output-dir=dist `
        --output-filename="multiringstrobodiscgen-v$VERSION-$ARCH.exe" `
        --include-module=svgwrite `
        --include-module=svglib `
        --include-module=tempfile `
        --include-module=reportlab `
        --include-package=reportlab `
        --windows-console-mode=disable
}

$output_file = "dist\multiringstrobodiscgen-v$VERSION-$ARCH.exe"
Write-Output "The executable '$output_file' has been created."