import zipfile
import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Union, List

class OfficeMetadataExtractor:
    SUPPORTED_EXTENSIONS = ('.docx', '.xlsx', '.pptx')

    def __init__(self, source: Union[str, List[str]]):
        if isinstance(source, str):
            self.files = self._get_office_files_from_folder(source)
        elif isinstance(source, list):
            self.files = self._validate_file_list(source)
        else:
            raise ValueError("Source must be a folder path or a list of file paths.")

        self.custom_ns = {
            'vt': 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes',
            '': 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'
        }
        self.core_ns = {
            'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'dcterms': 'http://purl.org/dc/terms/',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

    def _get_office_files_from_folder(self, folder_path: str) -> List[str]:
        return [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(self.SUPPORTED_EXTENSIONS)
        ]

    def _validate_file_list(self, file_list: List[str]) -> List[str]:
        return [
            f for f in file_list
            if f.lower().endswith(self.SUPPORTED_EXTENSIONS) and os.path.isfile(f)
        ]

    def _extract_custom_properties(self, zip_ref) -> dict:
        data = {}
        try:
            if 'docProps/custom.xml' in zip_ref.namelist():
                with zip_ref.open('docProps/custom.xml') as xml_file:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    for prop in root.findall('property', self.custom_ns):
                        name = prop.attrib.get('name')
                        value_node = list(prop)[0]
                        data[name] = value_node.text
        except Exception:
            pass
        return data

    def _extract_core_properties(self, zip_ref) -> dict:
        data = {}
        try:
            if 'docProps/core.xml' in zip_ref.namelist():
                with zip_ref.open('docProps/core.xml') as xml_file:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    for elem in root:
                        tag = elem.tag.split('}')[-1]
                        data[tag] = elem.text
        except Exception:
            pass
        return data

    def _get_file_metadata(self, file_path: str) -> dict:
        try:
            stat = os.stat(file_path)
            return {
                "file_size": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat()
            }
        except Exception:
            return {}

    def get_metadata(self) -> dict:
        result = {}
        for file_path in self.files:
            filename = os.path.basename(file_path)
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    result[filename] = {
                        "custom": self._extract_custom_properties(zip_ref),
                        "core": self._extract_core_properties(zip_ref),
                        "file_info": self._get_file_metadata(file_path)
                    }
            except Exception:
                result[filename] = {
                    "custom": {},
                    "core": {},
                    "file_info": self._get_file_metadata(file_path)
                }
        return result