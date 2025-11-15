# Changelog

All notable changes to the HEIC Image Converter project will be documented in this file.

## [2.0.0] - 2025-11-15

### Added
- **PNG/JPEG Format Selection**: Users can now choose between PNG and JPEG output formats
- **JPEG Quality Control**: Adjustable quality slider (50-100) for JPEG conversions
- **Smart Format Handling**: Automatic RGB conversion for transparent images when saving as JPEG
- **Dynamic UI**: Quality slider automatically appears/hides based on selected format
- **Enhanced Status Messages**: Conversion messages now indicate the selected format and quality

### Changed
- Application title updated to "HEIC Image Converter" (from "HEIC to PNG Converter")
- Window height increased from 400px to 450px to accommodate new controls
- Conversion function renamed to `convert_heic_to_image` for better clarity
- **Default format changed to JPEG** (was PNG in earlier iterations)
- JPEG radio button now appears first, PNG second
- Quality slider visible by default
- Updated all documentation to reflect dual-format support

### Technical Details
- Default output format: JPEG (Quality 95)
- JPEG conversions use white background for images with transparency
- Both PNG and JPEG outputs are optimized for best compression
- File extensions: `.png` for PNG, `.jpg` for JPEG

## [1.0.0] - 2025-11-15

### Initial Release
- Convert HEIC images to PNG format
- Batch folder conversion
- Individual file selection
- Parallel processing (up to 4 workers)
- Auto-deletion of original HEIC files
- Progress tracking and detailed results
- Compiled standalone Windows executable
- Modern GUI interface with tkinter

### Features
- Support for `.heic`, `.HEIC`, `.heif`, `.HEIF` input files
- Optimized PNG output
- Real-time status updates
- Error handling and reporting
- No installation required (standalone .exe)

