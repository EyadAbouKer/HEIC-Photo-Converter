# Build Instructions for HEIC Photo Converter

This document explains how to compile the HEIC Photo Converter into a standalone executable.

## Prerequisites

- Python 3.8 or higher
- Virtual environment with dependencies installed
- PyInstaller (will be installed during build process)

## Building the Executable

### Method 1: Using the Build Script (Recommended)

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install PyInstaller if not already installed
pip install pyinstaller

# Build using the spec file
pyinstaller build_config.spec --clean
```

### Method 2: Direct PyInstaller Command

If you don't want to use the spec file, you can build directly:

```bash
.\venv\Scripts\Activate.ps1

pyinstaller --name "HEIC_Converter" ^
    --onefile ^
    --windowed ^
    --hidden-import PIL._tkinter_finder ^
    --hidden-import pillow_heif ^
    --hidden-import _pillow_heif ^
    --add-binary "venv/Lib/site-packages/_pillow_heif.cp313-win_amd64.pyd;." ^
    --add-binary "venv/Lib/site-packages/libde265-*.dll;." ^
    --add-binary "venv/Lib/site-packages/libheif-*.dll;." ^
    --add-binary "venv/Lib/site-packages/libgcc_s_seh-1-*.dll;." ^
    --add-binary "venv/Lib/site-packages/libstdc++-6-*.dll;." ^
    --add-binary "venv/Lib/site-packages/libwinpthread-1-*.dll;." ^
    --add-binary "venv/Lib/site-packages/libx265-*.dll;." ^
    heic_converter.py
```

## Build Output

After successful compilation, you'll find:

- `dist/HEIC_Converter.exe` - The standalone executable (~23 MB)
- `build/` - Temporary build files (can be deleted)

## Distribution

To share the application:

1. Navigate to the `dist/` folder
2. Share the `HEIC_Converter.exe` file
3. Optionally include `README_DISTRIBUTION.txt` for user instructions

The executable is completely standalone and requires:
- Windows 10 or later (64-bit)
- No Python installation
- No additional dependencies

## Build Configuration

The `build_config.spec` file contains:

- **Name**: HEIC_Converter
- **Type**: Windowed application (no console)
- **Mode**: Single file executable (--onefile)
- **Includes**: All necessary DLLs from pillow-heif
- **Hidden imports**: PIL._tkinter_finder, pillow_heif, _pillow_heif

## Troubleshooting

### Build fails with "Module not found"
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that pillow-heif is properly installed

### Executable doesn't start
- Try building without `--onefile` for debugging
- Check `warn-build_config.txt` in the build folder for warnings
- Ensure all DLL files are being bundled

### Missing dependencies in executable
- Add the module to `hiddenimports` in `build_config.spec`
- Manually add DLLs using `--add-binary` or update the spec file

## Clean Build

To perform a clean build:

```bash
# Remove old build artifacts
Remove-Item -Recurse -Force build, dist

# Build fresh
pyinstaller build_config.spec --clean
```

## File Size Optimization

The current build is ~23 MB. To reduce size:

1. Remove unused Pillow plugins (not recommended)
2. Use UPX compression (already enabled)
3. Build without `--onefile` to create a folder distribution

## Adding an Icon

To add a custom icon:

1. Create or obtain a `.ico` file
2. Update `build_config.spec`:
   ```python
   icon='path/to/your/icon.ico'
   ```
3. Rebuild

## Notes

- Build time: ~30 seconds on average hardware
- The executable includes Python interpreter and all dependencies
- First launch may trigger Windows SmartScreen (normal for unsigned apps)
- Consider code signing for production distribution

