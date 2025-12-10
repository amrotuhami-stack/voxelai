#!/usr/bin/env python3
"""
Cephalometric Landmark Schema
Maps landmarks across different datasets to a unified schema

Datasets:
- ISBI 2015: 19 landmarks
- Aariz/CEPHA29: 29 landmarks  
- CL-Detection 2024: 53 landmarks

Common landmarks across all datasets are mapped to a unified schema.
"""

# ISBI 2015 Landmarks (19)
ISBI_LANDMARKS = {
    0: "Sella",
    1: "Nasion",
    2: "Orbitale",
    3: "Porion",
    4: "A-point",
    5: "B-point",
    6: "Pogonion",
    7: "Menton",
    8: "Gnathion",
    9: "Gonion",
    10: "Lower Incisal Incision",
    11: "Upper Incisal Incision",
    12: "Upper Lip",
    13: "Lower Lip",
    14: "Subnasale",
    15: "Soft Tissue Pogonion",
    16: "Posterior Nasal Spine",
    17: "Anterior Nasal Spine",
    18: "Articulare",
}

# Aariz/CEPHA29 Landmarks (29) - includes ISBI 19 + 10 additional
AARIZ_LANDMARKS = {
    0: "Sella",
    1: "Nasion",
    2: "Orbitale",
    3: "Porion",
    4: "A-point",
    5: "B-point",
    6: "Pogonion",
    7: "Menton",
    8: "Gnathion",
    9: "Gonion",
    10: "Lower Incisal Incision",
    11: "Upper Incisal Incision",
    12: "Upper Lip",
    13: "Lower Lip",
    14: "Subnasale",
    15: "Soft Tissue Pogonion",
    16: "Posterior Nasal Spine",
    17: "Anterior Nasal Spine",
    18: "Articulare",
    # Additional landmarks in Aariz
    19: "Basion",
    20: "Upper Molar Mesial",
    21: "Upper Molar Distal",
    22: "Lower Molar Mesial",
    23: "Lower Molar Distal",
    24: "Pronasale",
    25: "Columella",
    26: "Soft Tissue Nasion",
    27: "Glabella",
    28: "Cervical Point",
}

# CL-Detection 2024 Landmarks (53) - most comprehensive
CL_DETECTION_LANDMARKS = {
    # Skeletal landmarks
    0: "Sella",
    1: "Nasion",
    2: "Orbitale",
    3: "Porion",
    4: "A-point",
    5: "B-point",
    6: "Pogonion",
    7: "Menton",
    8: "Gnathion",
    9: "Gonion",
    10: "Articulare",
    11: "Basion",
    12: "Anterior Nasal Spine",
    13: "Posterior Nasal Spine",
    14: "Pterygomaxillare",
    15: "Bolton Point",
    16: "Opisthion",
    17: "Condylion",
    18: "Ramus Point",
    # Dental landmarks
    19: "Upper Incisal Edge",
    20: "Upper Incisal Apex",
    21: "Lower Incisal Edge",
    22: "Lower Incisal Apex",
    23: "Upper Molar Mesial",
    24: "Upper Molar Distal",
    25: "Lower Molar Mesial",
    26: "Lower Molar Distal",
    27: "Upper Molar Occlusal",
    28: "Lower Molar Occlusal",
    # Soft tissue landmarks
    29: "Soft Tissue Nasion",
    30: "Pronasale",
    31: "Subnasale",
    32: "Upper Lip",
    33: "Lower Lip",
    34: "Soft Tissue Pogonion",
    35: "Soft Tissue Menton",
    36: "Columella",
    37: "Glabella",
    38: "Cervical Point",
    # Cervical spine
    39: "C2 Anterior Superior",
    40: "C2 Anterior Inferior",
    41: "C2 Posterior Superior",
    42: "C2 Posterior Inferior",
    43: "C3 Anterior Superior",
    44: "C3 Anterior Inferior",
    45: "C3 Posterior Superior",
    46: "C3 Posterior Inferior",
    47: "C4 Anterior Superior",
    48: "C4 Anterior Inferior",
    49: "C4 Posterior Superior",
    50: "C4 Posterior Inferior",
    # Calibration
    51: "Ruler Start",
    52: "Ruler End",
}

# =============================================================================
# UNIFIED SCHEMA - Maps all datasets to common landmark IDs
# =============================================================================

# Canonical landmark names (normalized)
CANONICAL_LANDMARKS = {
    # Core skeletal (0-18)
    "sella": 0,
    "nasion": 1,
    "orbitale": 2,
    "porion": 3,
    "a_point": 4,
    "b_point": 5,
    "pogonion": 6,
    "menton": 7,
    "gnathion": 8,
    "gonion": 9,
    "articulare": 10,
    "basion": 11,
    "ans": 12,  # Anterior Nasal Spine
    "pns": 13,  # Posterior Nasal Spine
    "pterygomaxillare": 14,
    "bolton": 15,
    "condylion": 16,
    
    # Dental (17-26)
    "upper_incisal_edge": 17,
    "upper_incisal_apex": 18,
    "lower_incisal_edge": 19,
    "lower_incisal_apex": 20,
    "upper_molar_mesial": 21,
    "upper_molar_distal": 22,
    "lower_molar_mesial": 23,
    "lower_molar_distal": 24,
    "upper_molar_occlusal": 25,
    "lower_molar_occlusal": 26,
    
    # Soft tissue (27-38)
    "soft_nasion": 27,
    "glabella": 28,
    "pronasale": 29,
    "columella": 30,
    "subnasale": 31,
    "upper_lip": 32,
    "lower_lip": 33,
    "soft_pogonion": 34,
    "soft_menton": 35,
    "cervical_point": 36,
    
    # Cervical spine (37-48)
    "c2_ant_sup": 37,
    "c2_ant_inf": 38,
    "c2_post_sup": 39,
    "c2_post_inf": 40,
    "c3_ant_sup": 41,
    "c3_ant_inf": 42,
    "c3_post_sup": 43,
    "c3_post_inf": 44,
    "c4_ant_sup": 45,
    "c4_ant_inf": 46,
    "c4_post_sup": 47,
    "c4_post_inf": 48,
}

# Total unified landmarks
NUM_UNIFIED_LANDMARKS = 49

# =============================================================================
# MAPPING FROM EACH DATASET TO UNIFIED SCHEMA
# =============================================================================

# ISBI 2015 -> Unified (19 landmarks)
ISBI_TO_UNIFIED = {
    0: 0,   # Sella
    1: 1,   # Nasion
    2: 2,   # Orbitale
    3: 3,   # Porion
    4: 4,   # A-point
    5: 5,   # B-point
    6: 6,   # Pogonion
    7: 7,   # Menton
    8: 8,   # Gnathion
    9: 9,   # Gonion
    10: 19, # Lower Incisal -> lower_incisal_edge
    11: 17, # Upper Incisal -> upper_incisal_edge
    12: 32, # Upper Lip
    13: 33, # Lower Lip
    14: 31, # Subnasale
    15: 34, # Soft Tissue Pogonion
    16: 13, # PNS
    17: 12, # ANS
    18: 10, # Articulare
}

# Aariz -> Unified (29 landmarks)
AARIZ_TO_UNIFIED = {
    **ISBI_TO_UNIFIED,  # Include all ISBI mappings
    19: 11,  # Basion
    20: 21,  # Upper Molar Mesial
    21: 22,  # Upper Molar Distal
    22: 23,  # Lower Molar Mesial
    23: 24,  # Lower Molar Distal
    24: 29,  # Pronasale
    25: 30,  # Columella
    26: 27,  # Soft Tissue Nasion
    27: 28,  # Glabella
    28: 36,  # Cervical Point
}

# CL-Detection 2024 -> Unified (53 landmarks, many map directly)
CL_DETECTION_TO_UNIFIED = {
    0: 0,    # Sella
    1: 1,    # Nasion
    2: 2,    # Orbitale
    3: 3,    # Porion
    4: 4,    # A-point
    5: 5,    # B-point
    6: 6,    # Pogonion
    7: 7,    # Menton
    8: 8,    # Gnathion
    9: 9,    # Gonion
    10: 10,  # Articulare
    11: 11,  # Basion
    12: 12,  # ANS
    13: 13,  # PNS
    14: 14,  # Pterygomaxillare
    15: 15,  # Bolton
    17: 16,  # Condylion
    19: 17,  # Upper Incisal Edge
    20: 18,  # Upper Incisal Apex
    21: 19,  # Lower Incisal Edge
    22: 20,  # Lower Incisal Apex
    23: 21,  # Upper Molar Mesial
    24: 22,  # Upper Molar Distal
    25: 23,  # Lower Molar Mesial
    26: 24,  # Lower Molar Distal
    27: 25,  # Upper Molar Occlusal
    28: 26,  # Lower Molar Occlusal
    29: 27,  # Soft Tissue Nasion
    30: 29,  # Pronasale
    31: 31,  # Subnasale
    32: 32,  # Upper Lip
    33: 33,  # Lower Lip
    34: 34,  # Soft Tissue Pogonion
    35: 35,  # Soft Tissue Menton
    36: 30,  # Columella
    37: 28,  # Glabella
    38: 36,  # Cervical Point
    39: 37,  # C2 landmarks...
    40: 38,
    41: 39,
    42: 40,
    43: 41,
    44: 42,
    45: 43,
    46: 44,
    47: 45,
    48: 46,
    49: 47,
    50: 48,
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_unified_landmark_name(unified_id: int) -> str:
    """Get canonical name for unified landmark ID"""
    for name, id in CANONICAL_LANDMARKS.items():
        if id == unified_id:
            return name
    return f"landmark_{unified_id}"


def get_dataset_mapping(dataset: str) -> dict:
    """Get mapping from dataset landmark IDs to unified IDs"""
    mappings = {
        "isbi2015": ISBI_TO_UNIFIED,
        "aariz": AARIZ_TO_UNIFIED,
        "cl-detection-2024": CL_DETECTION_TO_UNIFIED,
    }
    return mappings.get(dataset, {})


def get_common_landmarks() -> list:
    """Get landmarks present in ALL datasets (intersection)"""
    isbi_unified = set(ISBI_TO_UNIFIED.values())
    aariz_unified = set(AARIZ_TO_UNIFIED.values())
    cl_unified = set(CL_DETECTION_TO_UNIFIED.values())
    
    common = isbi_unified & aariz_unified & cl_unified
    return sorted(list(common))


def get_landmark_coverage():
    """Show which datasets have which landmarks"""
    coverage = {}
    
    for unified_id in range(NUM_UNIFIED_LANDMARKS):
        name = get_unified_landmark_name(unified_id)
        coverage[unified_id] = {
            "name": name,
            "isbi2015": unified_id in ISBI_TO_UNIFIED.values(),
            "aariz": unified_id in AARIZ_TO_UNIFIED.values(),
            "cl_detection": unified_id in CL_DETECTION_TO_UNIFIED.values(),
        }
    
    return coverage


if __name__ == "__main__":
    print("=" * 60)
    print("CEPHALOMETRIC LANDMARK SCHEMA")
    print("=" * 60)
    
    print(f"\nTotal unified landmarks: {NUM_UNIFIED_LANDMARKS}")
    print(f"\nDataset coverage:")
    print(f"  - ISBI 2015: {len(ISBI_TO_UNIFIED)} landmarks")
    print(f"  - Aariz: {len(AARIZ_TO_UNIFIED)} landmarks")
    print(f"  - CL-Detection 2024: {len(CL_DETECTION_TO_UNIFIED)} landmarks")
    
    common = get_common_landmarks()
    print(f"\nCommon landmarks (in ALL datasets): {len(common)}")
    for lid in common:
        print(f"  [{lid:2d}] {get_unified_landmark_name(lid)}")
    
    print("\n" + "=" * 60)
    print("LANDMARK COVERAGE MATRIX")
    print("=" * 60)
    
    coverage = get_landmark_coverage()
    print(f"{'ID':>3} {'Name':<25} {'ISBI':^6} {'Aariz':^6} {'CL-Det':^6}")
    print("-" * 50)
    for lid, info in coverage.items():
        isbi = "✓" if info["isbi2015"] else "-"
        aariz = "✓" if info["aariz"] else "-"
        cl = "✓" if info["cl_detection"] else "-"
        print(f"{lid:>3} {info['name']:<25} {isbi:^6} {aariz:^6} {cl:^6}")
