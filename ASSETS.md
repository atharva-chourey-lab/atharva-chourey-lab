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

## v2 fidelity upgrade (2026-11-17)

Build script: `~/workspace/github-dashboard/build_brain_assets_v2.py` (same venv;
run log: `build_brain_assets_v2_log.json`). The NiiVue set now ships at **full
resolution** — the v1 caveat about the downsampled label reading 2.67 cm³ no longer
applies to the shipped overlays: volumes quoted from the shipped NIfTIs are now the
true full-res volumes.

| File | Size | v2 change |
|---|---|---|
| `lion_brain_mri.nii.gz` | 13,264,819 B (13.3 MB) | **Full-res copy, byte-identical to source** (MD5 `cfe7c60ef0e2fba76f3832d8637d1de0`): 276×334×209, 0.3 mm iso — replaces the ×2-downsampled 138×167×104 / 0.6 mm version. Under the ~25 MB web budget. |
| `lion_hippocampus.nii.gz` | 42,043 B | **Full-res catalogue label, byte-identical copy** (MD5 `a48a94a56061a7b89f3824c2cfab1fbc`), same grid as the MRI. Voxel count verified on reload: **74,899 → 2.022 cm³** — the headline volume is now exact in the shipped overlay. |
| `lion_telencephalon.nii.gz` | 272,280 B | **Full-res catalogue label, byte-identical copy** (MD5 `5429f29c5efbda8dda5acd0c849f66e1`), same grid. 5,392,604 voxels → 145.6 cm³. |
| `lion_hippocampus_surface.glb` | 2,362,232 B (2.4 MB) | Rebuilt from the full-res label: marching cubes step 1 + light Taubin smoothing (λ=0.5, ν=−0.53, 5 iterations). 45,393 verts / 90,834 faces, red vertex colour, watertight; mesh volume 1,973 mm³ (MC + smoothing sit ~2.4% under the 2,022 mm³ voxel count — expected surface-estimate shrinkage). Verified loading in trimesh. |
| `lion_brain_surface.glb` | 3,291,232 B (3.3 MB) | Rebuilt from the lab Otsu mask (`outputs/lion_brainmask_otsu.npy`, 6,965,911 voxels → 188.08 cm³) at **full resolution — no ×2 pre-downsample**, coordinates via the full MRI affine (v1 used axis scaling + origin only). 63,106 verts / 126,920 faces, grey — 2.2× the v1 mesh. Marching-cubes step 3: step 1 produced a 33.9 MB GLB and step 2 a 7.96 MB GLB (6.14 MB even with stored normals dropped), both over the 5 MB budget, and the venv has no quadric-decimation library, so step 3 was the finest step that fits. Not watertight: the Otsu mask touches the volume border and contains small satellite components (345 at this sampling) — same character as v1, unchanged. Verified loading in trimesh. |
| `rhino_profile_chart.png` | 143,955 B, 1600×600 px | **New.** Mean within-specimen centred log₁₀ centroid-size profiles (complete-6 specimens) for all five living rhino species, computed from `goldmine-hunter/gold/morpho-ct/epmc-rhino5/profiles_all5_complete6.csv` (Mallet et al. 2019 landmark data). Bones ordered humerus, radius, ulna, femur, tibia, fibula; radius+ulna shaded and labelled "forearm". Cross-check: all 30 computed species×bone means match Table 2 of `papers/p6-rhino-forearm/paper.md` §3.3 to within rounding (max abs diff 4.7×10⁻⁵; spot values: *R. sondaicus* humerus +0.1586, fibula −0.2447; *D. bicornis* femur +0.1531 — all exact at 4 dp). The build script aborts before saving the chart if this check ever fails. |

- **Legacy backup:** the v1 downsampled NIfTIs were **moved, not deleted**, to
  `assets/legacy/` (`lion_brain_mri.nii.gz` 1,622,619 B, `lion_hippocampus.nii.gz`
  17,810 B, `lion_telencephalon.nii.gz` 89,635 B — all 138×167×104, 0.6 mm).
- **Verification:** all three shipped NIfTIs reload in nibabel with identical
  shape (276×334×209) and **exactly equal affines** (`np.array_equal` on the MRI
  vs each label); both GLBs reload in trimesh (`force='mesh'`).
- **Unchanged by v2:** `lion_hippocampus_fullres_crop.nii.gz` (still exact),
  slice montage and QC overlay PNGs, and the `.obj` interchange copies — note the
  OBJs are still the **v1** meshes; only the GLBs were rebuilt.

## Species Explorer (2026-11-17)

Per-species web assets for **all 37 Brain Catalogue species** in
`assets/species/<slug>/`, built by `~/workspace/github-dashboard/build_species_assets.py`
from `data/brain_catalogue_full/` (CC BY-NC 4.0, same licence terms as above).
Manifest: `assets/species/manifest.json` (37 entries; 87.3 MB total, per-species
folders 0.07–7.25 MB for lazy loading). Each folder holds `brain.nii.gz` (MRI
downsampled ×2 block-mean uint8; ×3 where ×2 exceeded ~3 MB — Bottlenose dolphin,
Giant panda, Giraffe, House mouse, Thylacine), one overlay NIfTI per **non-empty**
label on the identical downsampled grid (max-pool), `hippocampus.glb` where a real
hippocampus label exists (full-res marching cubes + Taubin smoothing, red, <5 MB),
and `brain.glb` where a whole-brain surface exists (below). Independent verification:
all 88 shipped NIfTIs reload in nibabel with shape/affine identical to their
species' `brain.nii.gz`; all 28 GLBs load in trimesh; zero failures.
The Zenodo subset in `data/brain_catalogue/` adds **no new species** (all 13 are
in the full set) but rescues one MRI (Plains zebra, below).

**Census — discrepancy found and reconciled.** Reproducing the audit census by
voxel count over all 71 structure-label files (Atlas whole-brain masks counted
separately: 13 files, all real) gives **48 real / 23 empty**, not the paper's
53 / 18. The sealed census (processing log 2026-11-16, Goldmine Hunter sweep
`species-sweep-20261116-230812.json`) voxel-checked only 56 of the 71 files —
every checked file agrees with this recount (39 real / 17 empty, zero
disagreements) — plus the Galago hippocampus noted empty in the same log
(= 18 empty), and carried the other 15 unchecked files as real by subtraction
(71 − 18 = 53). Five of those 15 are zero-voxel **Striatum** files the sweep
never checked (Baboon, Crab-eating macaque, Gorilla, Human, Rhesus macaque),
which accounts exactly for the difference. Full reconciliation in the manifest
(`census.paper_census`). All 23 empty files were re-verified zero-voxel with an
independent counter (unique value [0] in every case).

### Per-species status

- **3D-viewable — catalogue mesh (11):** Black rhinoceros, Cat, Cheetah, Ferret,
  Human, Leopard, Lion, Nile crocodile, Orangutan, Sloth bear, Slow loris —
  `brain.glb` converted from the catalogue's own `mesh.ply`.
  (Inventory discrepancy: `outputs/braincatalogue_inventory.json` records
  `mesh: None` for every species, yet 11 `mesh.ply` files exist on disk; the
  filesystem was followed.)
- **3D-viewable — derived mesh (7):** Blackbuck, Bottlenose dolphin, Chimpanzee,
  Gorilla, Red kangaroo, Red-necked wallaby, Red squirrel — no `mesh.ply`;
  `brain.glb` derived by the lab from the catalogue Atlas whole-brain mask label
  (marching cubes + Taubin, grey), provenance recorded in the manifest.
- **Hippocampus-only 3D (2):** Giant panda, Giraffe — no whole-brain surface,
  but a hippocampus mesh. (Hippocampus meshes also ship for Black rhinoceros,
  Cat, Cheetah, Ferret, Leopard, Lion, Sloth bear and Red kangaroo alongside
  their brain meshes — 10 `hippocampus.glb` in total.)
- **Volume-only (17):** Baboon, Crab-eating macaque, Demidoff's dwarf Galago,
  Gibbon, Gray wolf, Grey-cheeked mangabey, House mouse, La Plata dolphin,
  Night monkey, Nursehound, Okapi, Ostrich, Plains zebra, Platypus,
  Rhesus macaque, Thylacine, White-headed capuchin — MRI + label overlays, no mesh.
- **No-data: none.** Every one of the 37 species has a real MRI after two
  documented fallbacks: the website copies of the Lion and Plains zebra MRIs in
  `brain_catalogue_full/` are 0-byte files — the Lion uses the MD5-verified
  Zenodo 44855 original in `data/lion/`, the zebra the Zenodo-subset scan in
  `data/brain_catalogue/` (grid verified identical to its Telencephalon label).

### Honesty notes

- **Empty hippocampus labels (no overlay, no mesh, no volume):** Baboon,
  Blackbuck, Bottlenose dolphin, Chimpanzee, Crab-eating macaque, Demidoff's
  dwarf Galago, Gorilla, Gray wolf, Grey-cheeked mangabey, Human, La Plata
  dolphin, Orangutan, Ostrich, Red-necked wallaby, Rhesus macaque, Slow loris,
  Thylacine, White-headed capuchin (18 species). The manifest's
  `hippocampus_cm3_mri` for the 10 species with real labels matches
  `outputs/cross_species_volumes_v3.csv` wherever v3 classes the value
  `catalogue_label` (all matched within 0.01 cm³; no flags). Published
  histological comparators exist in the record only for **Lion (4.496 cm³)** and
  **Leopard (3.121 cm³)**, both Reep et al. 2007 via paper p1 §3.3; all other
  species carry `hippocampus_cm3_histology: null` — never guessed.
  `audited` in the manifest = membership of paper p1's verified hippocampus
  set (10 species); `in_paper_qc_fit_set` = the QC fit set (8).
- **Audit-excluded junk, counted in the census but NOT shipped:** Night monkey
  hippocampus (1 voxel), Okapi hippocampus (272-voxel sliver), Red squirrel
  "hippocampus" (file duplicates the whole-brain Atlas mask — its computed
  757.5 cm³ in the manifest is that mask's volume, flagged
  `hippocampus_excluded_junk`, not a hippocampus), Bottlenose dolphin
  corpus callosum (900 voxels, placeholder-class).
- **Forensic flags carried, data shipped as-is:** Sloth bear hippocampus label
  is the paper's confirmed artifact (both main components on the same side of
  the midline); Giraffe hippocampus label is unilateral. Both are flagged in
  the manifest and were excluded from the paper's fit.
- **Template-header labels:** Bottlenose dolphin Cerebellum, Chimpanzee
  Cerebellum and Red kangaroo Hippocampus carry a generic template affine
  (identical origin/zooms across species) that does not match their MRI — no
  overlay shipped for any of them; the kangaroo hippocampus mesh was built in
  the label file's own coordinates and is flagged.
- **Orientation-mismatched labels:** Night monkey Cerebrum + Telencephalon and
  Nile crocodile Telencephalon share their MRI's shape/zooms/origin but differ
  in axis signs/permutation — not index-aligned, so no overlay shipped
  (no silent flipping or resampling was applied).
- **Repairs/fallbacks of record:** Nile crocodile MRI lacks NIfTI magic bytes
  and loads only after an in-memory magic repair (voxel data unchanged); six
  non-uint8-range MRIs (Demidoff's dwarf Galago, Gibbon, Grey-cheeked mangabey,
  Night monkey, Rhesus macaque, White-headed capuchin) were rescaled to uint8
  by 99.9th-percentile normalisation — all noted per species in the manifest.
- **Not mammals:** Nile crocodile (reptile), Nursehound (shark) and Ostrich
  (bird) are in the catalogue and were built like the rest; the manifest flags
  each. Scientific names are recorded only where the project record gives one
  (Lion *Panthera leo*, Human *Homo sapiens*, Black rhinoceros *Diceros
  bicornis*, Ferret *Mustela putorius*); all other entries use the directory
  name, per the no-invention rule.

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
