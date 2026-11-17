#!/usr/bin/env python
"""Build web assets for the Lost Atlas dashboard from the lab's REAL processed data.
Sources (all in ~/workspace/brain-scan-comparison):
  - Lion MRI: data/lion/MRI-n4.nii.gz  (Brain Catalogue, Zenodo 44855, CC BY-NC 4.0)
  - Lion hippocampus/telencephalon labels: data/brain_catalogue_full/Lion/*.nii.gz
    (recovered from braincatalogue.org; same grid/affine as the MRI)
  - Lion whole-brain surface: outputs/lion_brainmask_otsu.npy (the LAB's own Otsu mask)
No synthetic data. Downsampling: factor 2 (0.3 -> 0.6 mm); MRI block-mean,
labels max-pool (nearest-equivalent, preserves thin structures better than decimation).
"""
import os, json
import numpy as np
import nibabel as nib
from skimage import measure
import trimesh

SRC = os.path.expanduser("~/workspace/brain-scan-comparison")
OUT = os.path.expanduser("~/workspace/github-dashboard/assets")
os.makedirs(OUT, exist_ok=True)
F = 2  # downsample factor

def block_reduce_mean(a):
    x, y, z = (s // F * F for s in a.shape)
    a = a[:x, :y, :z].astype(np.float32)
    return a.reshape(x//F, F, y//F, F, z//F, F).mean(axis=(1, 3, 5))

def block_reduce_max(a):
    x, y, z = (s // F * F for s in a.shape)
    a = a[:x, :y, :z]
    return a.reshape(x//F, F, y//F, F, z//F, F).max(axis=(1, 3, 5))

def ds_affine(img):
    aff = img.affine.copy()
    aff[:3, :3] *= F
    return aff

log = {}

# --- 1. Lion MRI, downsampled ---
mri = nib.load(f"{SRC}/data/lion/MRI-n4.nii.gz")
mri_ds = block_reduce_mean(mri.get_fdata()).round().clip(0, 255).astype(np.uint8)
out = nib.Nifti1Image(mri_ds, ds_affine(mri)); out.header.set_data_dtype(np.uint8)
p = f"{OUT}/lion_brain_mri.nii.gz"; nib.save(out, p)
log["lion_brain_mri.nii.gz"] = dict(shape=list(mri_ds.shape), zooms=[0.6]*3, bytes=os.path.getsize(p),
                                   source_shape=list(mri.shape))

# --- 2/3. Labels on the matched downsampled grid ---
for name, srcf in [("lion_hippocampus", "Hippocampus"), ("lion_telencephalon", "Telencephalon")]:
    im = nib.load(f"{SRC}/data/brain_catalogue_full/Lion/{srcf}.nii.gz")
    d = (im.get_fdata() > 0).astype(np.uint8)
    full_vol = float(d.sum() * np.prod(im.header.get_zooms()[:3]) / 1000.0)
    ds = block_reduce_max(d)
    o = nib.Nifti1Image(ds, ds_affine(im)); o.header.set_data_dtype(np.uint8)
    p = f"{OUT}/{name}.nii.gz"; nib.save(o, p)
    log[f"{name}.nii.gz"] = dict(shape=list(ds.shape), bytes=os.path.getsize(p),
                                 fullres_volume_cm3=round(full_vol, 3),
                                 downsampled_volume_cm3=round(float(ds.sum() * 0.6**3 / 1000.0), 3))
    if name == "lion_hippocampus":
        hipp_full = d; hipp_img = im
        # full-res cropped label (exact voxel count preserved)
        idx = np.argwhere(d > 0); lo = np.maximum(idx.min(0) - 4, 0); hi = np.minimum(idx.max(0) + 5, d.shape)
        crop = d[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        caff = im.affine.copy(); caff[:3, 3] = nib.affines.apply_affine(im.affine, lo)
        o = nib.Nifti1Image(crop, caff); o.header.set_data_dtype(np.uint8)
        p = f"{OUT}/lion_hippocampus_fullres_crop.nii.gz"; nib.save(o, p)
        log["lion_hippocampus_fullres_crop.nii.gz"] = dict(shape=list(crop.shape), bytes=os.path.getsize(p),
                                                           voxels=int(crop.sum()), volume_cm3=round(full_vol, 3))

# --- 4. Hippocampus surface mesh (marching cubes on the FULL-RES label, mm coords) ---
verts, faces, normals, _ = measure.marching_cubes(hipp_full.astype(np.float32), level=0.5, step_size=1)
verts_mm = nib.affines.apply_affine(hipp_img.affine, verts)
mesh = trimesh.Trimesh(vertices=verts_mm, faces=faces, vertex_normals=normals, process=False)
mesh.visual.vertex_colors = np.tile(np.array([230, 60, 40, 255], dtype=np.uint8), (len(verts_mm), 1))
for ext in ("glb", "obj"):
    p = f"{OUT}/lion_hippocampus_surface.{ext}"; mesh.export(p)
    log[f"lion_hippocampus_surface.{ext}"] = dict(bytes=os.path.getsize(p), vertices=int(len(verts_mm)), faces=int(len(faces)))

# --- 5. Whole-brain surface mesh from the LAB's own Otsu mask ---
mask = np.load(f"{SRC}/outputs/lion_brainmask_otsu.npy")
mds = block_reduce_max(mask.astype(np.uint8)).astype(np.float32)
verts, faces, normals, _ = measure.marching_cubes(mds, level=0.5, step_size=2)
verts_mm = verts * (0.3 * F) + nib.affines.apply_affine(mri.affine, [0, 0, 0])
mesh = trimesh.Trimesh(vertices=verts_mm, faces=faces, vertex_normals=normals, process=False)
mesh.visual.vertex_colors = np.tile(np.array([190, 190, 200, 255], dtype=np.uint8), (len(verts_mm), 1))
for ext in ("glb", "obj"):
    p = f"{OUT}/lion_brain_surface.{ext}"; mesh.export(p)
    log[f"lion_brain_surface.{ext}"] = dict(bytes=os.path.getsize(p), vertices=int(len(verts_mm)), faces=int(len(faces)))

# --- 6. Real slice montage: MRI slices through hippocampus centroid + label overlay ---
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
mri_full = mri.get_fdata()
cen = np.argwhere(hipp_full > 0).mean(0).astype(int)
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, (plane, sl, title) in zip(axes, [
        (0, cen[0], f"Sagittal x={cen[0]}"), (1, cen[1], f"Coronal y={cen[1]}"), (2, cen[2], f"Axial z={cen[2]}")]):
    img = np.take(mri_full, sl, axis=plane); lab = np.take(hipp_full, sl, axis=plane)
    ax.imshow(np.rot90(img), cmap="gray")
    ax.imshow(np.rot90(np.ma.masked_where(lab == 0, lab)), cmap="Reds", alpha=0.85)
    ax.set_title(title); ax.axis("off")
fig.suptitle("Lion MRI (Brain Catalogue, Zenodo 44855) with catalogue hippocampus label (red) — real data, slices through label centroid")
fig.tight_layout()
p = f"{OUT}/lion_hippocampus_slices.png"; fig.savefig(p, dpi=150)
log["lion_hippocampus_slices.png"] = dict(bytes=os.path.getsize(p), centroid_vox=[int(c) for c in cen])

print(json.dumps(log, indent=1))
