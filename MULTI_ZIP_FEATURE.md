# Multi-ZIP Batch Processing Feature

## Overview

The AEM URL Converter has been enhanced to support processing multiple GlobalLink ZIP files simultaneously. This feature allows users to upload multiple ZIP files at once and receive a consolidated report with automatic deduplication.

## Key Features

### 🚀 Multi-File Upload
- Select multiple ZIP files at once using the file uploader
- Process all files in a single batch operation
- Real-time progress feedback during processing

### 🔄 Smart Deduplication
- Automatically removes duplicate URLs across ZIP files
- **Latest file wins** strategy for conflicts
- Preserves source file tracking for transparency

### 📊 Enhanced Reporting
- **Source File Tracking**: Shows which ZIP file each URL came from
- **Comprehensive Statistics**: Total files processed, unique URLs found
- **Source Column**: Optional column in tables when multiple files are processed

### 📁 Source File Management
- Each AEM link tracks its source ZIP file
- Source information displayed in tables and HTML reports
- File names cleaned (removes .zip extension for display)

## Technical Implementation

### Core Changes

#### 1. Enhanced Data Model (`core/models.py`)
```python
@dataclass
class AEMLink:
    url: str
    path: str
    language: str
    source_zip: str = None  # NEW: Track source ZIP file
```

#### 2. Batch Processing (`services/file_processor.py`)
```python
class BatchProcessor:
    def process_multiple_zips(self, zip_files: List) -> ProcessingResult:
        # Process multiple ZIP files
        # Automatic deduplication
        # Source tracking
```

#### 3. Enhanced UI (`app.py`)
```python
uploaded_files = st.file_uploader(
    "Upload GlobalLink ZIP file(s)",
    type="zip",
    accept_multiple_files=True  # NEW: Multiple file support
)
```

### Deduplication Logic

When processing multiple ZIP files, duplicate URLs (same path) are automatically removed using the **latest file wins** strategy:

1. **Path-based Deduplication**: URLs with identical paths are considered duplicates
2. **Latest File Priority**: When duplicates are found, the version from the later-processed file is kept
3. **Source Tracking**: The winning URL retains its source ZIP information
4. **User Notification**: Deduplication statistics are shown in warnings

## User Interface

### File Upload
- **Single File**: Works exactly as before
- **Multiple Files**: Select multiple ZIP files using Ctrl+Click or Cmd+Click
- **Visual Feedback**: File count and processing status displayed

### Results Display
- **Summary Tab**: Shows total files processed and unique URLs found
- **Language Tabs**: Korean and Japanese results with optional source column
- **Source Column**: Automatically shown when multiple files are processed
- **Processed Files**: Expandable list showing all processed file names

### HTML Reports
- **Combined Reports**: Single report containing results from all ZIP files
- **Source Information**: Source files listed in report header
- **Source Column**: Optional column in HTML tables for multiple files
- **Smart Naming**: Generated filenames indicate multiple file processing

## Configuration

No additional configuration required. The feature is automatically available and adapts based on the number of files uploaded.

## Backward Compatibility

✅ **Fully Backward Compatible**
- Single file processing works exactly as before
- Existing templates and configurations remain valid
- No breaking changes to APIs or data structures

## Example Workflows

### Single File (Existing Workflow)
1. Upload one ZIP file
2. View results in tabs
3. Download HTML report

### Multiple Files (New Workflow)
1. Select multiple ZIP files (Ctrl+Click)
2. Upload all files at once
3. View consolidated results with source tracking
4. Download comprehensive HTML report

## Error Handling

- **Individual File Errors**: Errors in one ZIP don't affect others
- **Validation**: Each file validated independently
- **Warning Messages**: Deduplication statistics and processing warnings
- **Graceful Degradation**: Falls back to single file processing if BatchProcessor unavailable

## Performance Considerations

- **Memory Efficient**: Files processed sequentially, not loaded all at once
- **Progress Feedback**: Real-time processing status updates
- **Optimized Deduplication**: Hash-based duplicate detection for performance

## Version Information

- **Feature Version**: 2.1.0
- **Release Date**: 2025-09-18
- **Branch**: feature/multiple-zip-support
- **Base Branch**: solid

## Files Modified

### Core Files
- `core/models.py` - Enhanced AEMLink with source tracking
- `services/file_processor.py` - Enhanced BatchProcessor with deduplication
- `app.py` - Multi-file UI support

### Presentation Layer
- `presentation/df_builder.py` - Source column support
- `presentation/html_renderer.py` - Multi-file HTML rendering

### Infrastructure
- `di_container.py` - Updated frontmatter and metadata
- `main.py` - Updated version information

### Documentation
- `MULTI_ZIP_FEATURE.md` - This feature documentation

## Testing

The implementation has been tested with:
- ✅ Model creation with source ZIP tracking
- ✅ Dictionary conversion including source information
- ✅ BatchProcessor availability and instantiation
- ✅ Deduplication logic with latest-file-wins strategy
- ✅ Import validation across all modules

## Future Enhancements

Potential future improvements:
- **Parallel Processing**: Process multiple ZIP files in parallel
- **Advanced Deduplication**: User-configurable deduplication strategies
- **File Comparison**: Side-by-side comparison of duplicate URLs from different files
- **Batch Export**: Export source-specific reports for each ZIP file