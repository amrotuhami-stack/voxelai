"""
Unified Label Schema for Dental AI
Maps all datasets to a common format for multi-dataset training
"""

# FDI Numbering System (Fédération Dentaire Internationale)
# Format: <quadrant><tooth_position>
# Quadrants: 1=UR, 2=UL, 3=LL, 4=LR (adult), 5=UR, 6=UL, 7=LL, 8=LR (child)
# Positions: 1-8 (central incisor to 3rd molar)

FDI_TOOTH_NAMES = {
    # Upper Right (Quadrant 1) - Adult
    "11": "Upper Right Central Incisor",
    "12": "Upper Right Lateral Incisor",
    "13": "Upper Right Canine",
    "14": "Upper Right First Premolar",
    "15": "Upper Right Second Premolar",
    "16": "Upper Right First Molar",
    "17": "Upper Right Second Molar",
    "18": "Upper Right Third Molar (Wisdom)",
    
    # Upper Left (Quadrant 2) - Adult
    "21": "Upper Left Central Incisor",
    "22": "Upper Left Lateral Incisor",
    "23": "Upper Left Canine",
    "24": "Upper Left First Premolar",
    "25": "Upper Left Second Premolar",
    "26": "Upper Left First Molar",
    "27": "Upper Left Second Molar",
    "28": "Upper Left Third Molar (Wisdom)",
    
    # Lower Left (Quadrant 3) - Adult
    "31": "Lower Left Central Incisor",
    "32": "Lower Left Lateral Incisor",
    "33": "Lower Left Canine",
    "34": "Lower Left First Premolar",
    "35": "Lower Left Second Premolar",
    "36": "Lower Left First Molar",
    "37": "Lower Left Second Molar",
    "38": "Lower Left Third Molar (Wisdom)",
    
    # Lower Right (Quadrant 4) - Adult
    "41": "Lower Right Central Incisor",
    "42": "Lower Right Lateral Incisor",
    "43": "Lower Right Canine",
    "44": "Lower Right First Premolar",
    "45": "Lower Right Second Premolar",
    "46": "Lower Right First Molar",
    "47": "Lower Right Second Molar",
    "48": "Lower Right Third Molar (Wisdom)",
    
    # Deciduous (Baby) Teeth - Upper Right (Quadrant 5)
    "51": "Upper Right Deciduous Central Incisor",
    "52": "Upper Right Deciduous Lateral Incisor",
    "53": "Upper Right Deciduous Canine",
    "54": "Upper Right Deciduous First Molar",
    "55": "Upper Right Deciduous Second Molar",
    
    # Deciduous - Upper Left (Quadrant 6)
    "61": "Upper Left Deciduous Central Incisor",
    "62": "Upper Left Deciduous Lateral Incisor",
    "63": "Upper Left Deciduous Canine",
    "64": "Upper Left Deciduous First Molar",
    "65": "Upper Left Deciduous Second Molar",
    
    # Deciduous - Lower Left (Quadrant 7)
    "71": "Lower Left Deciduous Central Incisor",
    "72": "Lower Left Deciduous Lateral Incisor",
    "73": "Lower Left Deciduous Canine",
    "74": "Lower Left Deciduous First Molar",
    "75": "Lower Left Deciduous Second Molar",
    
    # Deciduous - Lower Right (Quadrant 8)
    "81": "Lower Right Deciduous Central Incisor",
    "82": "Lower Right Deciduous Lateral Incisor",
    "83": "Lower Right Deciduous Canine",
    "84": "Lower Right Deciduous First Molar",
    "85": "Lower Right Deciduous Second Molar",
}

# Tooth type categories
TOOTH_TYPES = {
    "incisor": ["11", "12", "21", "22", "31", "32", "41", "42", 
                "51", "52", "61", "62", "71", "72", "81", "82"],
    "canine": ["13", "23", "33", "43", "53", "63", "73", "83"],
    "premolar": ["14", "15", "24", "25", "34", "35", "44", "45"],
    "molar": ["16", "17", "18", "26", "27", "28", "36", "37", "38", "46", "47", "48",
              "54", "55", "64", "65", "74", "75", "84", "85"],
}

# Lesion/Pathology types
LESION_TYPES = {
    # From DENTEX
    "caries": {
        "id": 1,
        "color": [255, 0, 0],  # Red
        "severity": ["early", "moderate", "deep"],
    },
    "deep_caries": {
        "id": 2,
        "color": [200, 0, 0],  # Dark Red
        "parent": "caries",
    },
    "periapical_lesion": {
        "id": 3,
        "color": [255, 165, 0],  # Orange
    },
    "impacted": {
        "id": 4,
        "color": [128, 0, 128],  # Purple
    },
    
    # Additional from other datasets
    "missing": {
        "id": 5,
        "color": [128, 128, 128],  # Gray
    },
    "root_canal": {
        "id": 6,
        "color": [0, 0, 255],  # Blue
    },
    "restoration": {
        "id": 7,
        "color": [0, 255, 255],  # Cyan
        "subtypes": ["filling", "crown", "implant", "bridge"],
    },
    "fracture": {
        "id": 8,
        "color": [255, 255, 0],  # Yellow
    },
}

# Quadrant definitions
QUADRANTS = {
    1: {"name": "Upper Right", "teeth": ["11", "12", "13", "14", "15", "16", "17", "18"]},
    2: {"name": "Upper Left", "teeth": ["21", "22", "23", "24", "25", "26", "27", "28"]},
    3: {"name": "Lower Left", "teeth": ["31", "32", "33", "34", "35", "36", "37", "38"]},
    4: {"name": "Lower Right", "teeth": ["41", "42", "43", "44", "45", "46", "47", "48"]},
}

# Unified annotation format (COCO-style)
UNIFIED_ANNOTATION_TEMPLATE = {
    "info": {
        "description": "Unified Dental AI Dataset",
        "version": "1.0",
        "year": 2024,
    },
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": [],
}

def get_category_list():
    """Generate COCO-style category list"""
    categories = []
    
    # Tooth categories (by FDI number)
    for fdi, name in FDI_TOOTH_NAMES.items():
        categories.append({
            "id": int(fdi),
            "name": f"tooth_{fdi}",
            "supercategory": "tooth",
            "fdi_number": fdi,
            "display_name": name,
        })
    
    # Lesion categories
    for lesion_name, lesion_info in LESION_TYPES.items():
        categories.append({
            "id": 100 + lesion_info["id"],
            "name": lesion_name,
            "supercategory": "lesion",
            "color": lesion_info["color"],
        })
    
    return categories


def map_dentex_to_unified(dentex_annotation: dict) -> dict:
    """Convert DENTEX annotation format to unified format"""
    # DENTEX format: {quadrant, enumeration, diagnosis}
    unified = {
        "tooth_id": None,
        "tooth_type": None,
        "bbox": None,
        "lesions": [],
        "geometry_type": "bbox",
    }
    
    # Map quadrant + enumeration to FDI number
    quadrant = dentex_annotation.get("quadrant")
    enum = dentex_annotation.get("enumeration")
    if quadrant and enum:
        unified["tooth_id"] = f"{quadrant}{enum}"
        
        # Determine tooth type
        for ttype, fdi_list in TOOTH_TYPES.items():
            if unified["tooth_id"] in fdi_list:
                unified["tooth_type"] = ttype
                break
    
    # Map diagnosis
    diagnosis = dentex_annotation.get("diagnosis")
    if diagnosis:
        if diagnosis in LESION_TYPES:
            unified["lesions"].append({
                "type": diagnosis,
                "id": LESION_TYPES[diagnosis]["id"],
            })
    
    # Copy bbox
    unified["bbox"] = dentex_annotation.get("bbox")
    
    return unified


def map_odontoai_to_unified(odontoai_annotation: dict) -> dict:
    """Convert OdontoAI annotation format to unified format"""
    # OdontoAI uses different category IDs
    # Need to map their 52 categories to FDI
    unified = {
        "tooth_id": None,
        "tooth_type": None,
        "bbox": None,
        "lesions": [],
        "geometry_type": "bbox",
    }
    
    # TODO: Implement OdontoAI category mapping
    # Their format needs to be reverse-engineered from their JSON
    
    return unified


# Export schema as JSON for external tools
def export_schema(output_path: str = "label_schema.json"):
    """Export the unified schema as JSON"""
    import json
    
    schema = {
        "fdi_teeth": FDI_TOOTH_NAMES,
        "tooth_types": TOOTH_TYPES,
        "lesion_types": {k: {"id": v["id"], "color": v["color"]} 
                         for k, v in LESION_TYPES.items()},
        "quadrants": QUADRANTS,
        "categories": get_category_list(),
    }
    
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)
    
    print(f"Schema exported to {output_path}")
    return schema


if __name__ == "__main__":
    # Test export
    export_schema()
    print(f"Total tooth categories: {len(FDI_TOOTH_NAMES)}")
    print(f"Total lesion types: {len(LESION_TYPES)}")
