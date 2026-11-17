# Dashboard assets — Workstream A (Lost Atlas / brain data)

Built 2026-11-17 from the lab's real processed data in `~/workspace/brain-scan-comparison/`.
**No stock, synthetic, or AI-generated brain imagery is used anywhere.** Every asset below
traces to a named source file. Build script: `~/workspace/github-dashboard/build_brain_assets.py`
(run with the project venv `brain-scan-comparison/.venv`, nibabel 5.5 / scikit-image 0.26 / trimesh 5.2.1).

## Licence / redistribution verdict — READ FIRST

- **Lion MRI (Zenodo record 44855)** — Brain Catalogue, Santin, Herbin & Toro (2016):
  **CC BY-NC 4.0** (record-level licence, recorded in `data/lion/PROVENANCE.md`).
  A downsampled copy **may** be redistributed **non-commercially, with attribution**
  ("Brain Catalogue — Santin, Herbin & Toro 2016, Zenodo 44855, CC BY-NC 4.0").
  The NC term is binding: these assets must not be used commercially.
- **Lion label files (Hippocampus / Telencephalon) and `mesh.ply`** were **not** in the
  Zenodo records; the lab recovered them from the project's own website
  (braincatalogue.org/data/Lion/). No separate licence file for the website files exists
  in the project record. The published paper treats the catalogue's scans *and* labels as
  distributed under CC BY-NC 4.0, and the paper itself **did not redistribute source data**
  ("Data are not redistributed with this paper"). Verdict applied here: the label-derived
  assets below are prepared for the lab's own **non-commercial** dashboard under the same
  CC BY-NC 4.0 attribution, on the paper's stated basis. If the dashboard ever becomes
  commercial, or if counsel reads the website files as unlicensed, the label-derived
  assets (hippocampus/telencephalon NIfTIs + hippocampus mesh) must come down; the
  lab's own derived products (brain-surface mesh from our Otsu mask, slice montage,
  QC overlay, all statistics) are unaffected.
- **M-CRIB 2.0 newborn data** (OSF `4vthr` / `mnwv9`): CC BY 4.0 — redistributable with
  attribution, but **no newborn asset was built** (see "Not shown").

## Assets in `assets/`

| File | Size | What it is | Source |
|---|---|---|---|
| `lion_brain_mri.nii.gz` | 1,622,619 B (1.6 MB) | Lion structural MRI for a NiiVue viewer. 138×167×104, 0.6 mm iso, uint8 | Downsampled ×2 (block-mean) from `data/lion/MRI-n4.nii.gz` (276×334×209, 0.3 mm, Zenodo 44855, CC BY-NC 4.0) |
| `lion_hippocampus.nii.gz` | 17,810 B | Hippocampus label overlay, **same grid as the MRI asset above** (load as NiiVue overlay) | Downsampled ×2 (max-pool) from `data/brain_catalogue_full/Lion/Hippocampus.nii.gz` — the catalogue label that yielded the headline **2.02 cm³** (74,899 voxels × 0.3³ mm³) |
| `lion_hippocampus_fullres_crop.nii.gz` | 54,996 B | The same label at **full 0.3 mm resolution**, cropped to its bounding box + 4-voxel pad, affine preserved. Exact voxel count 74,899 → **2.022 cm³** | Same source label, crop only — no resampling |
| `lion_telencephalon.nii.gz` | 89,635 B | Telencephalon label overlay, matched grid (context structure, 145.6 cm³ at full res) | Downsampled ×2 (max-pool) from `data/brain_catalogue_full/Lion/Telencephalon.nii.gz` |
| `lion_hippocampus_surface.glb` | 2,362,176 B (2.3 MB) | Surface mesh of the hippocampus label for three.js (45,393 verts / 90,834 faces, red vertex colour, coordinates in mm via the source affine) | Marching cubes (level 0.5, step 1) on the **full-resolution** catalogue label |
| `lion_hippocampus_surface.obj` | 8,563,634 B (8.2 MB) | Same mesh, OBJ interchange copy | Same |
| `lion_brain_surface.glb` | 1,472,752 B (1.4 MB) | Whole-brain surface for three.js (28,417 verts / 56,326 faces, grey) | Marching cubes on **the lab's own** Otsu whole-brain mask (`outputs/lion_brainmask_otsu.npy`, 188.1 cm³), downsampled ×2, MC step 2. Our derived product — not catalogue data |
| `lion_brain_surface.obj` | 5,291,361 B (5.1 MB) | Same mesh, OBJ copy | Same |
| `lion_hippocampus_slices.png` | 502,560 B | Sagittal/coronal/axial MRI slices through the hippocampus-label centroid (voxel 140, 179, 116) with the label in red — honest 2D fallback if the 3D viewer fails | Rendered from the two source files above with matplotlib |
| `lion_hippocampus_qc_overlay.png` | ~210 KB | The project's own QC overlay figure from the original analysis | Copied verbatim from `outputs/qc_lion_hippocampus_overlay.png` |

All files are < 20 MB. NIfTI assets verified to reload in nibabel; GLBs verified to load in trimesh.

### Processing notes / honesty caveats
- Downsampling the MRI is block-mean (intensity-preserving); labels use max-pool so thin
  label parts survive. **Side effect: the downsampled label's naive voxel-count volume
  reads 2.67 cm³, not 2.02 cm³** (max-pool thickens boundaries). Display only — any volume
  quoted on the dashboard must come from the full-resolution label (2.022 cm³) or
  `lion_hippocampus_fullres_crop.nii.gz`, never from the downsampled overlay. Same effect,
  smaller, for telencephalon (154.2 vs 145.6 cm³).
- The two GLB meshes are standalone viewers; they were exported through slightly different
  coordinate paths (full affine vs mask grid) and are **not** guaranteed co-registered as
  overlays of each other. The NiiVue NIfTI pair *is* co-registered (identical grid/affine).
- The catalogue also ships a lion `mesh.ply` (982,247 B, website-recovered). It was **not**
  converted or shipped — the brain surface above is the lab's own mask instead.

## What is NOT shown, and why
- **No newborn/human brain volume.** The paper's other side is M-CRIB newborn data
  (CC BY 4.0, so licence is not the blocker) — it was out of this workstream's lion/atlas
  scope; a newborn asset can be built the same way on request.
- **No hippocampus for the 18 empty-placeholder species** — those label files contain
  zero voxels (the paper's audit finding: 53 usable of 71 label files). There is nothing
  real to render.
- **No dolphin hippocampus** — the catalogue label is an empty placeholder and the lab's
  own tracing attempt failed QC (`outputs/segmentations/bottlenose_tracing_v1_FAILED.nii.gz`);
  no volume was claimed, so nothing is rendered.
- **No D99-propagated lion hippocampus as "the" result** — the lab also produced a
  model-estimated propagation (`outputs/segmentations/Lion_hippocampus_D99formation_propagated.nii.gz`,
  1.789 cm³ at 1 mm, provisional). The headline 2.02 cm³ is the catalogue label; only that
  is visualised, to avoid mixing a model estimate with the measured label.
- **No other species' volumes** were prepared — the other 36 catalogue species exist
  locally (below) and can be added identically if the dashboard wants them.

## Full inventory of real data found (source project: `~/workspace/brain-scan-comparison/`)

- **Lion (the headline specimen)** — `data/lion/MRI-n4.nii.gz` (13,264,819 B, Zenodo 44855,
  MD5-verified, CC BY-NC 4.0); website-recovered `data/lion/atlas/` = `data/brain_catalogue_full/Lion/`:
  `Hippocampus.nii.gz` (42,043 B → 2.022 cm³), `Telencephalon.nii.gz` (145.6 cm³), `mesh.ply`;
  the website copy of the lion MRI arrived empty (0 B) and was not used.
- **Full Brain Catalogue** — `data/brain_catalogue_full/`: 37 species directories,
  121 NIfTI files (per-species MRI + labels: Hippocampus, Telencephalon/Cerebrum, Striatum,
  Cerebellum, Corpus_callosum, Neocortex, Atlas whole-brain masks), 11 `mesh.ply` files;
  census in `outputs/braincatalogue_inventory.json`: 71 label files audited, **53 real,
  18 empty placeholders**. Earlier 13-species Zenodo subset in `data/brain_catalogue/`
  (provenance in its `PROVENANCE.md`, CC BY-NC 4.0). Per-species volumes:
  `outputs/cross_species_volumes_v3.csv` (8 species with valid direct hippocampus labels).
- **Lab's own segmentations** — `outputs/segmentations/` (11 NIfTI): propagated hippocampi
  for human (6.85 cm³), chimpanzee, gorilla, gray wolf, red-necked wallaby (model-estimated,
  flagged provisional in the paper); D99-formation propagations for lion and leopard;
  the lab's own rhino tight delineation; the failed dolphin tracing (kept, labelled FAILED).
  Plus `outputs/lion_brainmask_otsu.npy` (lab Otsu mask) and ~25 QC overlay PNGs.
- **Human newborn** — `data/human_infant/`: 120 NIfTI (M-CRIB 2.0 T1/T2 + 94-region
  parcellations ×10 subjects; M-CRIB-WM), CC BY 4.0, provenance in `data/human_infant/PROVENANCE.md`.
- **Reference atlases (not catalogue data)** — `data/atlases/`: D99 macaque atlas v2.0
  (label volume + template + ~hundreds of GIFTI surfaces) and Harvard–Oxford atlases —
  used as propagation sources only; **not** redistributed here (their own terms apply).
  `data/proxies/` is the Catlas domestic-cat template — a labelled proxy, **never lion data**,
  and deliberately excluded from the assets.
- **Aquatic follow-up** — `aquatic/` (measurements CSV/JSON + QC sheet) and
  `outputs/dolphin_feasibility/` (~20 real slice-render PNGs of the bottlenose scan).
