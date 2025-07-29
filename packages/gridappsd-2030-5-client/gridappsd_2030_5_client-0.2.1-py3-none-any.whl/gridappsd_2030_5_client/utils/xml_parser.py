"""XML parsing utilities for IEEE 2030.5 client."""

import xml.etree.ElementTree as ET
from typing import Dict, Any


def parse_xml(xml_content: bytes) -> Dict:
    """
    Parse XML content into a dictionary.
    
    Args:
        xml_content: XML content as bytes
        
    Returns:
        Dictionary representation of XML
    """
    try:
        root = ET.fromstring(xml_content)
        # Create a dictionary with the root element name as the key
        # and the parsed content as the value
        return {root.tag: element_to_dict(root)}
    except Exception as e:
        raise ValueError(f"Failed to parse XML: {str(e)}")


def element_to_dict(element: ET.Element) -> Dict:
    """
    Convert XML element to dictionary.
    
    Args:
        element: XML element
        
    Returns:
        Dictionary representation
    """
    result = {}
    
    # Add attributes
    for key, value in element.attrib.items():
        result[f"@{key}"] = value
    
    # Add children
    for child in element:
        child_dict = element_to_dict(child)
        
        if child.tag in result:
            # If this tag already exists, convert to list or append
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_dict)
            else:
                result[child.tag] = [result[child.tag], child_dict]
        else:
            result[child.tag] = child_dict
    
    # Add text content
    if element.text and element.text.strip():
        if len(result) == 0:
            return element.text.strip()
        else:
            result["#text"] = element.text.strip()
    
    return result