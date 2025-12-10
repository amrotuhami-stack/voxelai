# Cephalometric Landmark Mapping

## Unified Schema (19 Common Landmarks)

The following landmarks are present in **ALL** merged datasets and used for training:

| Unified ID | Canonical Name | ISBI 2015 | Aariz | Description |
|------------|---------------|-----------|-------|-------------|
| 0 | sella | ✓ (0) | ✓ Sella | Center of sella turcica |
| 1 | nasion | ✓ (1) | ✓ Nasion | Frontonasal suture |
| 2 | orbitale | ✓ (2) | ✓ Orbitale | Lowest point of orbit |
| 3 | porion | ✓ (3) | ✓ Porion | Upper edge of external auditory meatus |
| 4 | a_point | ✓ (4) | ✓ A-point | Deepest point on maxilla |
| 5 | b_point | ✓ (5) | ✓ B-point | Deepest point on mandible |
| 6 | pogonion | ✓ (6) | ✓ Pogonion | Most anterior point of chin |
| 7 | menton | ✓ (7) | ✓ Menton | Lowest point of mandibular symphysis |
| 8 | gnathion | ✓ (8) | ✓ Gnathion | Most anterior-inferior point of chin |
| 9 | gonion | ✓ (9) | ✓ Gonion | Angle of mandible |
| 10 | articulare | ✓ (18) | ✓ Articulare | Junction of skull base and mandible |
| 12 | ans | ✓ (17) | ✓ Anterior Nasal Spine | Tip of anterior nasal spine |
| 13 | pns | ✓ (16) | ✓ Posterior Nasal Spine | Tip of posterior nasal spine |
| 17 | upper_incisal_edge | ✓ (11) | ✓ Upper Incisor Tip | Tip of upper central incisor |
| 19 | lower_incisal_edge | ✓ (10) | ✓ Lower Incisor Tip | Tip of lower central incisor |
| 31 | subnasale | ✓ (14) | ✓ Subnasale | Junction of nasal septum and upper lip |
| 32 | upper_lip | ✓ (12) | ✓ Labrale superius | Most anterior point of upper lip |
| 33 | lower_lip | ✓ (13) | ✓ Labrale inferius | Most anterior point of lower lip |
| 34 | soft_pogonion | ✓ (15) | ✓ Soft Tissue Pogonion | Soft tissue chin point |

---

## ISBI 2015 Landmark Mapping

| ISBI ID | ISBI Name | → Unified ID | Unified Name |
|---------|-----------|--------------|--------------|
| 0 | Sella | → 0 | sella |
| 1 | Nasion | → 1 | nasion |
| 2 | Orbitale | → 2 | orbitale |
| 3 | Porion | → 3 | porion |
| 4 | A-point | → 4 | a_point |
| 5 | B-point | → 5 | b_point |
| 6 | Pogonion | → 6 | pogonion |
| 7 | Menton | → 7 | menton |
| 8 | Gnathion | → 8 | gnathion |
| 9 | Gonion | → 9 | gonion |
| 10 | Lower Incisal Incision | → 19 | lower_incisal_edge |
| 11 | Upper Incisal Incision | → 17 | upper_incisal_edge |
| 12 | Upper Lip | → 32 | upper_lip |
| 13 | Lower Lip | → 33 | lower_lip |
| 14 | Subnasale | → 31 | subnasale |
| 15 | Soft Tissue Pogonion | → 34 | soft_pogonion |
| 16 | Posterior Nasal Spine | → 13 | pns |
| 17 | Anterior Nasal Spine | → 12 | ans |
| 18 | Articulare | → 10 | articulare |

---

## Aariz/CEPHA29 Landmark Mapping

| Aariz Name | → Unified ID | Unified Name | In Common Set? |
|------------|--------------|--------------|----------------|
| Sella | → 0 | sella | ✓ |
| Nasion | → 1 | nasion | ✓ |
| Orbitale | → 2 | orbitale | ✓ |
| Porion | → 3 | porion | ✓ |
| A-point | → 4 | a_point | ✓ |
| B-point | → 5 | b_point | ✓ |
| Pogonion | → 6 | pogonion | ✓ |
| Menton | → 7 | menton | ✓ |
| Gnathion | → 8 | gnathion | ✓ |
| Gonion | → 9 | gonion | ✓ |
| Articulare | → 10 | articulare | ✓ |
| Anterior Nasal Spine | → 12 | ans | ✓ |
| Posterior Nasal Spine | → 13 | pns | ✓ |
| Upper Incisor Tip | → 17 | upper_incisal_edge | ✓ |
| Lower Incisor Tip | → 19 | lower_incisal_edge | ✓ |
| Subnasale | → 31 | subnasale | ✓ |
| Labrale superius | → 32 | upper_lip | ✓ |
| Labrale inferius | → 33 | lower_lip | ✓ |
| Soft Tissue Pogonion | → 34 | soft_pogonion | ✓ |
| Condylion | → 16 | condylion | ✗ (Aariz only) |
| Upper Incisor Apex | → 18 | upper_incisal_apex | ✗ (Aariz only) |
| Lower Incisor Apex | → 20 | lower_incisal_apex | ✗ (Aariz only) |
| Upper Molar Cusp Tip | → 25 | upper_molar_occlusal | ✗ (Aariz only) |
| Lower Molar Cusp Tip | → 26 | lower_molar_occlusal | ✗ (Aariz only) |
| Pronasale | → 29 | pronasale | ✗ (Aariz only) |
| Soft Tissue Nasion | → 27 | soft_nasion | ✗ (Aariz only) |

---

## Merged Dataset Statistics

Total Images: 895
- ISBI 2015:  290 images (19 landmarks each)
- Aariz:      605 images (29 landmarks each, 19 used)

Split:
- Train: 463 images
- Val:   241 images
- Test:  191 images

Common Landmarks Used: 19
