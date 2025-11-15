# HEIC to PNG Converter

A simple and user-friendly Windows application to convert HEIC (High Efficiency Image Container) images to PNG format.

## Features

- 📁 **Batch Conversion**: Select a folder and convert all HEIC images at once
- 🖼️ **Selective Conversion**: Choose one or multiple specific HEIC files to convert
- 🎨 **Modern GUI**: Clean and intuitive interface built with tkinter
- ⚡ **Threaded Processing**: Non-blocking UI during conversion
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
4. Converted PNG files will be saved in the same location as the original files

**Option 2: Convert Selected Files**
1. Click the "🖼️ Convert Selected Files" button
2. Select one or multiple HEIC files from your file system
3. The selected files will be converted to PNG format
4. Converted PNG files will be saved in the same location as the original files

### Supported Formats

- Input: `.heic`, `.HEIC`, `.heif`, `.HEIF`
- Output: `.png`

## How It Works

1. The application uses the `pillow-heif` library to register HEIF format support with Pillow (PIL)
2. When you select files or a folder, the app scans for HEIC images
3. Each HEIC image is opened and converted to PNG format
4. The converted PNG file is saved with the same filename (different extension) in the same directory
5. Progress and results are displayed in real-time

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

## Future Enhancements

Possible improvements for future versions:
- Support for additional output formats (JPEG, WebP, etc.)
- Batch rename options
- Image quality settings
- Drag-and-drop functionality
- Conversion history

## Contributing

Feel free to fork this project and submit pull requests with improvements!
