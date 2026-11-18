#!/usr/bin/env python
"""Species Explorer asset layer for the Atharva Chourey Lab dashboard.

REAL DATA ONLY. Sources: ~/workspace/brain-scan-comparison/data/brain_catalogue_full/
(37 species dirs, Brain Catalogue, CC BY-NC 4.0) plus two documented fallbacks
where the website-recovered copy in brain_catalogue_full/ is a 0-byte file:
  - Lion MRI: data/lion/MRI-n4.nii.gz (the Zenodo 44855 original, MD5-verified)
  - Plains_zebra MRI: data/brain_catalogue/zebra.nii.gz (Zenodo subset; its grid
    matches the Plains_zebra Telencephalon label exactly, 243x313x227 @ 0.4 mm)

Per species with a real MRI, in assets/species/<slug>/:
  - brain.nii.gz: MRI downsampled x2 (block-mean, uint8; x3/x4 if needed to
    stay <= ~3 MB), 
  - one overlay NIfTI per NON-EMPTY label on the same downsampled grid
    (max-pool), named by structure slug,
  - hippocampus.glb: marching-cubes mesh from the FULL-RES hippocampus label
    (light Taubin smoothing, red vertex colour, <5 MB),
  - brain.glb: catalogue mesh.ply converted to GLB where one exists; else
    derived from a non-empty Atlas whole-brain mask label; else omitted.
Empty placeholder labels (0 voxels) are never shipped. Four audit-excluded
junk files (see EXCLUDED_JUNK, from outputs/cross_species_volumes_v3.csv) are
counted in the census but not shipped as overlays/meshes.
Writes assets/species/manifest.json. Run with the project venv.
"""
import os, json, sys
import numpy as np
import nibabel as nib
from skimage import measure
import trimesh

BASE = os.path.expanduser("~/workspace/brain-scan-comparison")
FULL = f"{BASE}/data/brain_catalogue_full"
OUTROOT = os.path.expanduser("~/workspace/github-dashboard/assets/species")
os.makedirs(OUTROOT, exist_ok=True)

INV = json.load(open(f"{BASE}/outputs/braincatalogue_inventory.json"))

# v3 cross-check table
import csv
V3 = {}
with open(f"{BASE}/outputs/cross_species_volumes_v3.csv") as f:
    for row in csv.DictReader(f):
        V3[row["species"]] = row

# Paper p1 (Lost Atlas): verified hippocampus set (10) and QC fit set (8),
# paper.md sections 3.1 / 2.3.
VERIFIED10 = {"Ferret", "Cat", "Cheetah", "Red_kangaroo", "Giant_panda",
              "Leopard", "Lion", "Sloth_bear", "Giraffe", "Black_rhinoceros"}
FIT8 = {"Black_rhinoceros", "Cat", "Cheetah", "Ferret", "Giant_panda",
        "Leopard", "Lion", "Red_kangaroo"}
# Published histological hippocampus comparators given in paper p1 (Reep et
# al. 2007, histological planimetry, shrinkage-corrected). Only these two
# catalogue species have one in the record; all others stay null.
HISTOLOGY = {
    "Lion": dict(value_cm3=4.496, source="Reep et al. 2007, histological planimetry (paper p1 section 3.3; specimen 62-79, 4,496.16 mm3 ~ 4.50 cm3)"),
    "Leopard": dict(value_cm3=3.121, source="Reep et al. 2007, histological planimetry (paper p1 section 3.3)"),
}
# Scientific names ONLY where present in the project record; else null.
SCIENTIFIC = {
    "Lion": "Panthera leo",                    # outputs/measurements.csv
    "Human": "Homo sapiens",                   # outputs/measurements.csv
    "Black_rhinoceros": "Diceros bicornis",    # REPORT.md
    "Ferret": "Mustela putorius",              # outputs/ferret_forensics.md
}
# Audit-excluded junk (outputs/cross_species_volumes_v3.csv notes): counted in
# the census as non-empty by voxels, but NOT shipped as overlay/mesh.
EXCLUDED_JUNK = {
    ("Night_monkey", "Hippocampus.nii.gz"): "EXCLUDED in project audit: 1 nonzero voxel - junk placeholder",
    ("Okapi", "Hippocampus.nii.gz"): "EXCLUDED in project audit: 272 nonzero voxels - sliver, not a structure",
    ("Red_squirrel", "Hippocampus.nii.gz"): "EXCLUDED in project audit: file duplicates the whole-brain Atlas mask - mislabeled",
    ("Bottlenose_dolphin", "Corpus_callosum.nii.gz"): "Project audit: placeholder-class file (nz=900), not a delineated corpus callosum",
}
MRI_FALLBACK = {
    "Lion": (f"{BASE}/data/lion/MRI-n4.nii.gz",
             "brain_catalogue_full/Lion/MRI-n4.nii.gz is a 0-byte website copy; "
             "used the MD5-verified Zenodo 44855 original in data/lion/ instead"),
    "Plains_zebra": (f"{BASE}/data/brain_catalogue/zebra.nii.gz",
                     "brain_catalogue_full/Plains_zebra/MRI.nii.gz is a 0-byte website copy; "
                     "used the Zenodo-subset scan in data/brain_catalogue/zebra.nii.gz "
                     "(grid verified identical to the species' Telencephalon label)"),
}
NON_MAMMALS = {"Nile_crocodile": "reptile (crocodilian) - in the catalogue, not a mammal",
               "Nursehound": "cartilaginous fish (shark) - in the catalogue, not a mammal",
               "Ostrich": "bird - in the catalogue, not a mammal"}

def load_img(path):
    """Load a NIfTI, squeezed to 3D. One source file (Nile_crocodile MRI)
    lacks the NIfTI magic bytes at offset 344, so nibabel refuses it; in
    that case repair the magic in a temp copy (voxel data untouched) and
    report repaired=True."""
    try:
        return nib.squeeze_image(nib.load(path)), False
    except Exception:
        import gzip
        raw = bytearray(gzip.open(path, "rb").read())
        raw[344:348] = b"n+1\x00"
        tmp = "/tmp/_repaired.nii"
        open(tmp, "wb").write(bytes(raw))
        return nib.squeeze_image(nib.load(tmp)), True

def slugify(dirname):
    s = dirname.lower().replace("_", "-").replace("'", "")
    return s

def struct_slug(fname):
    return fname.replace(".nii.gz", "").lower().replace("_", "-")

def block_reduce_mean(a, F):
    x, y, z = (s // F * F for s in a.shape)
    a = a[:x, :y, :z]
    return a.reshape(x//F, F, y//F, F, z//F, F).mean(axis=(1, 3, 5))

def block_reduce_max(a, F):
    x, y, z = (s // F * F for s in a.shape)
    a = a[:x, :y, :z]
    return a.reshape(x//F, F, y//F, F, z//F, F).max(axis=(1, 3, 5))

def ds_affine(img, F):
    aff = img.affine.copy()
    aff[:3, :3] *= F
    return aff

def count_nonzero(img):
    """Chunked nonzero count to bound memory on the largest volumes."""
    n = 0
    dataobj = img.dataobj
    step = 16
    for i in range(0, img.shape[0], step):
        slab = np.asanyarray(dataobj[i:i+step])
        n += int((slab > 0).sum())
    return n

def mesh_from_label(bool_vol, affine, color, budget=5_000_000):
    """Marching cubes at step 1, escalating until the GLB fits the budget."""
    vol = bool_vol.astype(np.float32)
    for step in (1, 2, 3, 4):
        verts, faces, normals, _ = measure.marching_cubes(vol, level=0.5, step_size=step)
        verts_mm = nib.affines.apply_affine(affine, verts)
        m = trimesh.Trimesh(vertices=verts_mm, faces=faces, vertex_normals=normals, process=False)
        trimesh.smoothing.filter_taubin(m, lamb=0.5, nu=-0.53, iterations=5)
        m.visual.vertex_colors = np.tile(np.array(color, dtype=np.uint8), (len(m.vertices), 1))
        tmp = "/tmp/_sp_mesh.glb"
        m.export(tmp)
        size = os.path.getsize(tmp)
        if size < budget or step == 4:
            return m, step, size
    return m, step, size

manifest_species = []
census = dict(label_files_excl_atlas=0, real_excl_atlas=0, empty_excl_atlas=0,
              atlas_files=0, atlas_real=0, atlas_empty=0)
flags = []

for dirname in sorted(INV.keys()):
    inv = INV[dirname]
    slug = slugify(dirname)
    sdir = os.path.join(FULL, dirname)
    entry = dict(slug=slug, directory=dirname,
                 common_name=dirname.replace("_", " "),
                 scientific_name=SCIENTIFIC.get(dirname),
                 notes=[])
    if dirname in NON_MAMMALS:
        entry["notes"].append(NON_MAMMALS[dirname])

    # ---- MRI source -------------------------------------------------------
    mri_name = inv.get("brain")
    mri_path = os.path.join(sdir, mri_name) if mri_name else None
    mri_note = None
    if (not mri_path or not os.path.exists(mri_path) or os.path.getsize(mri_path) == 0) \
            and dirname in MRI_FALLBACK:
        mri_path, mri_note = MRI_FALLBACK[dirname]
    has_mri = bool(mri_path and os.path.exists(mri_path) and os.path.getsize(mri_path) > 0)
    entry["has_mri"] = has_mri
    entry["mri_source_file"] = mri_path
    if mri_note:
        entry["notes"].append("MRI fallback: " + mri_note)
    mri_img = None
    if has_mri:
        mri_img, repaired = load_img(mri_path)
        if repaired:
            entry["notes"].append("MRI source file lacks NIfTI magic bytes; loaded via "
                                   "an in-memory magic repair - voxel data unchanged")
    if has_mri and count_nonzero(mri_img) == 0:
        has_mri = False
        entry["has_mri"] = False
        entry["notes"].append("MRI file loads but contains zero nonzero voxels - treated as no MRI")

    # ---- Labels: census + stats ------------------------------------------
    label_files = sorted(f for f in os.listdir(sdir)
                         if f.endswith(".nii.gz") and f != mri_name)
    structures = []
    label_imgs = {}
    for lf in label_files:
        limg, _rep = load_img(os.path.join(sdir, lf))
        label_imgs[lf] = limg
        vox = count_nonzero(limg)
        zooms = [float(z) for z in limg.header.get_zooms()[:3]]
        vol = float(vox * np.prod(zooms) / 1000.0)
        is_atlas = (lf == "Atlas.nii.gz")
        if is_atlas:
            census["atlas_files"] += 1
            census["atlas_real" if vox > 0 else "atlas_empty"] += 1
        else:
            census["label_files_excl_atlas"] += 1
            census["real_excl_atlas" if vox > 0 else "empty_excl_atlas"] += 1
        grid_match = None
        if mri_img is not None:
            grid_match = bool(list(limg.shape) == list(mri_img.shape)
                              and np.allclose(limg.affine, mri_img.affine))
        st = dict(name=lf.replace(".nii.gz", ""), slug=struct_slug(lf), file=lf,
                  voxels_fullres=vox, volume_cm3_fullres=round(vol, 4),
                  empty=bool(vox == 0), grid_matches_mri=grid_match,
                  shipped_overlay=False)
        junk = EXCLUDED_JUNK.get((dirname, lf))
        if junk:
            st["excluded_junk"] = junk
        structures.append(st)
    entry["structures"] = structures

    # ---- Hippocampus headline values + v3 cross-check ---------------------
    hip_st = next((s for s in structures if s["file"] == "Hippocampus.nii.gz"), None)
    entry["hippocampus_cm3_mri"] = (hip_st["volume_cm3_fullres"]
                                    if hip_st and not hip_st["empty"] else None)
    if hip_st and hip_st.get("excluded_junk"):
        entry["hippocampus_excluded_junk"] = hip_st["excluded_junk"]
    v3row = V3.get(dirname, {})
    cc = dict(v3_hippocampus_cm3=None, v3_data_class=v3row.get("data_class"),
              match=None)
    try:
        cc["v3_hippocampus_cm3"] = float(v3row["hippocampus_cm3"]) if v3row.get("hippocampus_cm3") else None
    except Exception:
        pass
    if cc["v3_data_class"] == "catalogue_label" and cc["v3_hippocampus_cm3"] is not None \
            and entry["hippocampus_cm3_mri"] is not None:
        cc["match"] = bool(abs(cc["v3_hippocampus_cm3"] - entry["hippocampus_cm3_mri"]) <= 0.01)
        if not cc["match"]:
            flags.append(f"{dirname}: hippocampus_cm3_mri {entry['hippocampus_cm3_mri']} "
                         f"!= cross_species_volumes_v3 {cc['v3_hippocampus_cm3']} (catalogue_label)")
            # red kangaroo corrupt-header case: recompute with MRI zooms
            if hip_st is not None and mri_img is not None:
                mz = [float(z) for z in mri_img.header.get_zooms()[:3]]
                alt = float(hip_st["voxels_fullres"] * np.prod(mz) / 1000.0)
                entry["notes"].append(
                    f"hippocampus volume with MRI zooms instead of the label file's own "
                    f"header zooms: {alt:.4f} cm3 (label header flagged corrupt in the "
                    f"paper, section 3.1); v3 value {cc['v3_hippocampus_cm3']}")
    entry["hippocampus_v3_crosscheck"] = cc
    entry["hippocampus_cm3_histology"] = HISTOLOGY.get(dirname)
    entry["audited"] = dirname in VERIFIED10
    entry["in_paper_qc_fit_set"] = dirname in FIT8
    if dirname == "Sloth_bear":
        entry["notes"].append("Paper p1 forensic QC: hippocampus label is an artifact "
                               "(both main components on the same side of the midline); "
                               "excluded from the paper's fit - shipped here flagged, as-is")
    if dirname == "Giraffe":
        entry["notes"].append("Paper p1 forensic QC: hippocampus label is unilateral "
                               "(second component 1.3% of the first); excluded from the "
                               "paper's fit - shipped here flagged, as-is")

    # ---- Web assets --------------------------------------------------------
    entry["downsample_factor"] = None
    entry["assets"] = {}
    mesh_info = dict(type="none", brain_glb=None, hippocampus_glb=None)
    if has_mri:
        odir = os.path.join(OUTROOT, slug)
        os.makedirs(odir, exist_ok=True)
        mri_arr = mri_img.get_fdata(dtype=np.float32)
        raw_max = float(mri_arr.max())
        rescaled = not (raw_max <= 255.0)
        F = 2
        while True:
            ds = block_reduce_mean(mri_arr, F)
            if rescaled:
                p999 = float(np.percentile(ds, 99.9)) or 1.0
                ds8 = (np.clip(ds, 0, p999) / p999 * 255.0).round().astype(np.uint8)
            else:
                ds8 = ds.round().clip(0, 255).astype(np.uint8)
            o = nib.Nifti1Image(ds8, ds_affine(mri_img, F))
            o.header.set_data_dtype(np.uint8)
            tmp = os.path.join(odir, "brain.nii.gz")
            nib.save(o, tmp)
            size = os.path.getsize(tmp)
            if size <= 3_200_000 or F >= 4:
                break
            F += 1
        del mri_arr
        entry["downsample_factor"] = F
        if rescaled:
            entry["notes"].append("MRI intensities rescaled to uint8 by 99.9th-percentile "
                                   "normalisation (source is not uint8-range)")
        entry["assets"]["brain.nii.gz"] = size
        brain_ds_shape = list(ds8.shape)
        brain_ds_affine = ds_affine(mri_img, F)

        # overlays for non-empty, grid-matched, non-junk labels
        for st in structures:
            if st["empty"] or st.get("excluded_junk") or not st["grid_matches_mri"]:
                if not st["empty"] and not st["grid_matches_mri"] and not st.get("excluded_junk"):
                    entry["notes"].append(f"{st['file']}: grid differs from MRI - no overlay shipped")
                continue
            limg = label_imgs[st["file"]]
            lab = (limg.get_fdata() > 0).astype(np.uint8)
            dsl = block_reduce_max(lab, F)
            del lab
            o = nib.Nifti1Image(dsl, brain_ds_affine)
            o.header.set_data_dtype(np.uint8)
            p = os.path.join(odir, st["slug"] + ".nii.gz")
            nib.save(o, p)
            st["shipped_overlay"] = True
            entry["assets"][st["slug"] + ".nii.gz"] = os.path.getsize(p)

        # hippocampus GLB from the FULL-RES label (label's own affine; an MRI
        # grid match is required for overlays, not for a standalone mesh)
        if hip_st and not hip_st["empty"] and not hip_st.get("excluded_junk"):
            if not hip_st["grid_matches_mri"]:
                entry["notes"].append(
                    "Hippocampus.nii.gz: header/grid does not match the MRI "
                    "(generic template header - identical affine in several "
                    "species' label files); no overlay shipped, mesh built in "
                    "the label file's own coordinates")
            limg = label_imgs["Hippocampus.nii.gz"]
            lab = (limg.get_fdata() > 0)
            try:
                m, step, gsize = mesh_from_label(lab, limg.affine, [230, 60, 40, 255])
                p = os.path.join(odir, "hippocampus.glb")
                m.export(p)
                mesh_info["hippocampus_glb"] = dict(file="hippocampus.glb", bytes=gsize,
                                                    mc_step_size=step,
                                                    vertices=int(len(m.vertices)),
                                                    faces=int(len(m.faces)))
                entry["assets"]["hippocampus.glb"] = gsize
            except Exception as e:
                entry["notes"].append(f"hippocampus mesh failed: {e}")
            del lab

        # brain GLB: catalogue mesh.ply first, else derived from Atlas mask
        ply = os.path.join(sdir, "mesh.ply")
        if os.path.exists(ply) and os.path.getsize(ply) > 0:
            try:
                pm = trimesh.load(ply, force="mesh")
                if len(getattr(pm, "faces", [])) == 0:
                    raise ValueError("mesh.ply has no faces")
                if getattr(pm.visual, "vertex_colors", None) is None:
                    pm.visual.vertex_colors = np.tile(
                        np.array([190, 190, 200, 255], dtype=np.uint8), (len(pm.vertices), 1))
                p = os.path.join(odir, "brain.glb")
                pm.export(p)
                mesh_info.update(type="catalogue", brain_glb=dict(
                    file="brain.glb", bytes=os.path.getsize(p),
                    source="catalogue mesh.ply (Brain Catalogue website file)",
                    vertices=int(len(pm.vertices)), faces=int(len(pm.faces))))
                entry["assets"]["brain.glb"] = os.path.getsize(p)
            except Exception as e:
                entry["notes"].append(f"catalogue mesh.ply conversion failed: {e}")
        if mesh_info["brain_glb"] is None:
            atlas_st = next((s for s in structures if s["file"] == "Atlas.nii.gz"), None)
            if atlas_st and not atlas_st["empty"] and atlas_st["grid_matches_mri"]:
                limg = label_imgs["Atlas.nii.gz"]
                lab = (limg.get_fdata() > 0)
                try:
                    m, step, gsize = mesh_from_label(lab, limg.affine, [190, 190, 200, 255])
                    p = os.path.join(odir, "brain.glb")
                    m.export(p)
                    mesh_info.update(type="derived", brain_glb=dict(
                        file="brain.glb", bytes=gsize, mc_step_size=step,
                        source="derived by the lab from the catalogue Atlas whole-brain mask label (marching cubes + Taubin smoothing)",
                        vertices=int(len(m.vertices)), faces=int(len(m.faces))))
                    entry["assets"]["brain.glb"] = gsize
                except Exception as e:
                    entry["notes"].append(f"Atlas-derived mesh failed: {e}")
                del lab
        if mesh_info["type"] == "none" and mesh_info["hippocampus_glb"]:
            mesh_info["type"] = "hippocampus-only"
    entry["mesh"] = mesh_info
    manifest_species.append(entry)
    print(f"{dirname}: mri={has_mri} F={entry['downsample_factor']} "
          f"mesh={mesh_info['type']} assets={entry['assets']}", flush=True)

# ---- Verification pass ------------------------------------------------------
ver = dict(nifti_checked=0, nifti_failures=[], glb_checked=0, glb_failures=[])
for e in manifest_species:
    if not e["has_mri"]:
        continue
    odir = os.path.join(OUTROOT, e["slug"])
    brain = nib.load(os.path.join(odir, "brain.nii.gz"))
    for fname in e["assets"]:
        p = os.path.join(odir, fname)
        try:
            if fname.endswith(".nii.gz"):
                im = nib.load(p)
                ver["nifti_checked"] += 1
                if fname != "brain.nii.gz":
                    assert list(im.shape) == list(brain.shape), "shape mismatch vs brain.nii.gz"
                    assert np.allclose(im.affine, brain.affine), "affine mismatch vs brain.nii.gz"
            elif fname.endswith(".glb"):
                m = trimesh.load(p, force="mesh")
                assert len(m.faces) > 0
                ver["glb_checked"] += 1
        except Exception as ex:
            (ver["nifti_failures"] if fname.endswith(".nii.gz") else ver["glb_failures"]).append(
                f"{e['slug']}/{fname}: {ex}")

manifest = dict(
    generated="2026-11-17",
    source="Brain Catalogue (Santin, Herbin & Toro 2016), CC BY-NC 4.0 - data/brain_catalogue_full/ plus documented fallbacks",
    census=dict(
        total_label_files_excl_atlas=census["label_files_excl_atlas"],
        real_label_files_excl_atlas=census["real_excl_atlas"],
        empty_label_files_excl_atlas=census["empty_excl_atlas"],
        atlas_mask_files=census["atlas_files"],
        atlas_mask_real=census["atlas_real"],
        atlas_mask_empty=census["atlas_empty"],
        note="The paper's 71-file census counts structure labels only; Atlas.nii.gz whole-brain mask files (13) are counted separately here.",
        paper_census=dict(real=53, empty=18,
            reconciliation="This recount voxel-checked all 71 files: 48 real / 23 empty. "
            "The sealed 53/18 (processing_log 2026-11-16, from the Goldmine Hunter sweep) "
            "voxel-checked only 56 of the 71 files - every checked file agrees with this "
            "recount (39 real / 17 empty, zero disagreements) - plus the Galago hippocampus "
            "called out empty in the same log (= 18 empty); the remaining 15 unchecked files "
            "were carried as real by subtraction (71 - 18 = 53). Five of those 15 are in fact "
            "zero-voxel Striatum files the sweep never checked (Baboon, Crab-eating macaque, "
            "Gorilla, Human, Rhesus macaque), which accounts exactly for the 53->48 and "
            "18->23 differences.")),
    definitions=dict(
        audited="Species is in paper p1's verified catalogue hippocampus set (10 species, paper.md section 3.1) before forensic exclusions",
        in_paper_qc_fit_set="Species is in paper p1's quality-controlled fit set (8 species, paper.md section 2.3)",
        hippocampus_cm3_histology="Published histological comparator from paper p1 / its sources only; null where the record gives none"),
    flags=flags,
    verification=ver,
    species=manifest_species,
)
with open(os.path.join(OUTROOT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1)
print(json.dumps(dict(census=manifest["census"], flags=flags, verification=ver), indent=1))
print("species entries:", len(manifest_species))
