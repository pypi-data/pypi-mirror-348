# Office Metadata Extractor

A Python library for extracting `custom.xml` and `core.xml` metadata from Microsoft Office files (.docx, .xlsx, .pptx). It also includes file-level metadata like file size and timestamps.

## Installation

```bash
pip install office_metadata_extractor
```

## Usage
```bash
from office_metadata_extractor import OfficeMetadataExtractor
```

### Option 1: Use a folder path
```bash
extractor = OfficeMetadataExtractor('path/to/folder')
metadata = extractor.get_metadata()
```

### Option 2: Use a list of files
```bash
files = ['doc1.docx', 'sheet1.xlsx']
extractor = OfficeMetadataExtractor(files)
metadata = extractor.get_metadata()
```

### Save to JSON
```bash
import json
with open('output.json', 'w') as f:
    json.dump(metadata, f, indent=4)
```

## Output
```
{
  "file.docx": {
    "custom": {
      "Property1": "Value1"
    },
    "core": {
      "title": "Document Title",
      "creator": "John"
    },
    "file_info": {
      "file_size": 10240,
      "modified_time": "2025-05-15T14:45:21",
      "created_time": "2025-05-10T10:12:03"
    }
  }
}
```
