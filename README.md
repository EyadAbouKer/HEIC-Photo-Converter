# HEIC to PNG Converter

A simple and user-friendly Windows application to convert HEIC (High Efficiency Image Container) images to PNG format.

## 🎯 Quick Start

**Two ways to use this application:**

### Option 1: Standalone Executable (Recommended for Users)
- Download `HEIC_Converter.exe` from the `dist/` folder
- Double-click to run - **no installation or Python required!**
- Perfect for sharing with friends and family

### Option 2: Run from Source (For Developers)
- Clone the repository and run with Python
- See installation instructions below

## Features

- 📁 **Batch Conversion**: Select a folder and convert all HEIC images at once
- 🖼️ **Selective Conversion**: Choose one or multiple specific HEIC files to convert
- 🎨 **Modern GUI**: Clean and intuitive interface built with tkinter
- ⚡ **Parallel Processing**: Up to 4 simultaneous conversions for faster performance
- 🚀 **Optimized Output**: PNG files are optimized for smaller file sizes
- 🗑️ **Auto-Cleanup**: Original HEIC files are automatically deleted after successful conversion
- 📊 **Progress Tracking**: Real-time status updates and conversion results
- ✅ **Error Handling**: Detailed feedback for successful and failed conversions

## Requirements

- Python 3.7 or higher
- Windows OS

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd HEIC-Photo-Converter
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Simply run the Python script:

```bash
python heic_converter.py
```

### Converting Images

**Option 1: Convert Entire Folder**
1. Click the "📁 Convert Folder" button
2. Select a folder containing HEIC images
3. The app will automatically find and convert all HEIC files in that folder
4. Converted PNG files will be saved in the same location
5. ⚠️ **Original HEIC files will be deleted** after successful conversion

**Option 2: Convert Selected Files**
1. Click the "🖼️ Convert Selected Files" button
2. Select one or multiple HEIC files from your file system
3. The selected files will be converted to PNG format
4. Converted PNG files will be saved in the same location
5. ⚠️ **Original HEIC files will be deleted** after successful conversion

### Supported Formats

- Input: `.heic`, `.HEIC`, `.heif`, `.HEIF`
- Output: `.png`

## How It Works

1. The application uses the `pillow-heif` library to register HEIF format support with Pillow (PIL)
2. When you select files or a folder, the app scans for HEIC images
3. Up to 4 HEIC images are processed simultaneously using parallel threading for faster conversion
4. Each HEIC image is opened and converted to optimized PNG format
5. The converted PNG file is saved with the same filename (different extension) in the same directory
6. **Original HEIC files are automatically deleted** after successful conversion
7. Progress and results are displayed in real-time
8. If a conversion fails, the original HEIC file is preserved

## Troubleshooting

### Import Errors
If you encounter import errors, make sure all dependencies are installed:
```bash
pip install --upgrade Pillow pillow-heif
```

### Conversion Failures
- Ensure the HEIC files are not corrupted
- Check that you have write permissions in the target directory
- Verify that the files are actually HEIC format (some files may have incorrect extensions)

## Dependencies

- **Pillow**: Python Imaging Library for image processing
- **pillow-heif**: HEIF/HEIC format support for Pillow

## License

This project is open source and available for personal and commercial use.

## Screenshots

The application provides:
- Large, easy-to-click buttons for both conversion modes
- A progress bar that animates during conversion
- A detailed results log showing each file's conversion status
- Color-coded status messages for quick feedback

## 📦 Compiled Executable

A standalone Windows executable is available in the `dist/` folder:

- **File**: `HEIC_Converter.exe` (~23 MB)
- **Requirements**: Windows 10 or later (64-bit)
- **No installation needed**: Just download and run!
- **Fully portable**: Can run from USB drives, network drives, etc.

### For End Users
Simply download `HEIC_Converter.exe` and double-click to run. No Python or dependencies required!

### For Developers - Building the Executable
To compile the application yourself:

1. Install PyInstaller: `pip install pyinstaller`
2. Run the build: `pyinstaller build_config.spec --clean`
3. Find the executable in the `dist/` folder

For detailed build instructions, see [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

## Future Enhancements

Possible improvements for future versions:
- Support for additional output formats (JPEG, WebP, etc.)
- Batch rename options
- Image quality settings
- Drag-and-drop functionality
- Conversion history
- Custom application icon
- Code signing for trusted distribution

## Contributing

Feel free to fork this project and submit pull requests with improvements!
