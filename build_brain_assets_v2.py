#!/usr/bin/env python
"""v2 fidelity upgrade for the Atharva Chourey Lab dashboard assets.

REAL DATA ONLY — no synthetic imagery. Sources (all in ~/workspace/brain-scan-comparison
unless noted):
  - Lion MRI, FULL resolution: data/lion/MRI-n4.nii.gz
    (Brain Catalogue, Zenodo 44855, CC BY-NC 4.0; 276x334x209, 0.3 mm iso)
  - Lion hippocampus / telencephalon labels, FULL resolution:
    data/brain_catalogue_full/Lion/{Hippocampus,Telencephalon}.nii.gz
    (same grid/affine as the MRI; hippocampus = 74,899 voxels -> 2.022 cm3)
  - Lion whole-brain surface: outputs/lion_brainmask_otsu.npy (the LAB's own Otsu
    mask, 188.1 cm3) at full resolution.
  - Rhino profile chart: ~/workspace/goldmine-hunter/gold/morpho-ct/epmc-rhino5/
    profiles_all5_complete6.csv (Mallet et al. 2019 landmark data, lab-computed
    within-specimen centred log10 centroid-size profiles, complete-6 specimens).
    Computed species means are cross-checked against Table 2 of
    ~/workspace/papers/p6-rhino-forearm/paper.md section 3; the script ABORTS
    before saving the chart if any value disagrees beyond rounding (5e-4).

Changes vs build_brain_assets.py (v1):
  - NiiVue set ships at FULL resolution (v1 shipped a x2-downsampled set).
    The v1 downsampled NIfTIs are moved to assets/legacy/ first, not deleted.
  - Hippocampus mesh rebuilt from the full-res label + light Taubin smoothing.
  - Whole-brain mesh rebuilt from the full-res Otsu mask (no x2 downsample;
    marching-cubes step 1, falling back to 2/3 only if the GLB would exceed
    5 MB) + light Taubin smoothing; coordinates via the full MRI affine
    (v1 used axis scaling + origin only).
Run with the project venv: ~/workspace/brain-scan-comparison/.venv/bin/python
"""
import os, json, shutil, sys
import numpy as np
import nibabel as nib
from skimage import measure
import trimesh

SRC = os.path.expanduser("~/workspace/brain-scan-comparison")
OUT = os.path.expanduser("~/workspace/github-dashboard/assets")
LEGACY = os.path.join(OUT, "legacy")
os.makedirs(OUT, exist_ok=True)
os.makedirs(LEGACY, exist_ok=True)

GLB_BUDGET = 5_000_000  # bytes
log = {}

# ----------------------------------------------------------------------------
# 0. Back up the v1 downsampled NIfTIs to assets/legacy/ (move, don't delete)
# ----------------------------------------------------------------------------
for fname in ("lion_brain_mri.nii.gz", "lion_hippocampus.nii.gz",
              "lion_telencephalon.nii.gz"):
    src_p, dst_p = os.path.join(OUT, fname), os.path.join(LEGACY, fname)
    if os.path.exists(dst_p):
        log.setdefault("legacy_backup", {})[fname] = "already in legacy/, left as-is"
        continue
    # Only back up if the current file is still the downsampled v1 grid;
    # if it is already full-res, a previous v2 run has done this step.
    shape = list(nib.load(src_p).shape)
    if shape == [276, 334, 209]:
        log.setdefault("legacy_backup", {})[fname] = "already full-res, no backup needed"
        continue
    shutil.move(src_p, dst_p)
    log.setdefault("legacy_backup", {})[fname] = dict(
        moved_to="assets/legacy/" + fname, shape=shape,
        bytes=os.path.getsize(dst_p))

# ----------------------------------------------------------------------------
# 1. FULL-RES NiiVue set — copied as-is (source files are already compact)
# ----------------------------------------------------------------------------
copies = {
    "lion_brain_mri.nii.gz": f"{SRC}/data/lion/MRI-n4.nii.gz",
    "lion_hippocampus.nii.gz": f"{SRC}/data/brain_catalogue_full/Lion/Hippocampus.nii.gz",
    "lion_telencephalon.nii.gz": f"{SRC}/data/brain_catalogue_full/Lion/Telencephalon.nii.gz",
}
for fname, src_p in copies.items():
    dst_p = os.path.join(OUT, fname)
    shutil.copy2(src_p, dst_p)
    log[fname] = dict(source=src_p, bytes=os.path.getsize(dst_p),
                      source_bytes=os.path.getsize(src_p))

# Verify: reload, shapes/affines match exactly, hippocampus voxel count.
mri = nib.load(os.path.join(OUT, "lion_brain_mri.nii.gz"))
hip_img = nib.load(os.path.join(OUT, "lion_hippocampus.nii.gz"))
tel_img = nib.load(os.path.join(OUT, "lion_telencephalon.nii.gz"))
hip = (hip_img.get_fdata() > 0)
hip_vox = int(hip.sum())
hip_vol = float(hip_vox * np.prod(hip_img.header.get_zooms()[:3]) / 1000.0)
verify = dict(
    shapes={k: list(v.shape) for k, v in
            [("mri", mri), ("hippocampus", hip_img), ("telencephalon", tel_img)]},
    zooms=[float(z) for z in mri.header.get_zooms()[:3]],
    affine_mri_eq_hippocampus=bool(np.array_equal(mri.affine, hip_img.affine)),
    affine_mri_eq_telencephalon=bool(np.array_equal(mri.affine, tel_img.affine)),
    hippocampus_voxels=hip_vox,
    hippocampus_volume_cm3=round(hip_vol, 4),
    telencephalon_voxels=int((tel_img.get_fdata() > 0).sum()),
    telencephalon_volume_cm3=round(float(
        (tel_img.get_fdata() > 0).sum()
        * np.prod(tel_img.header.get_zooms()[:3]) / 1000.0), 3),
)
assert verify["affine_mri_eq_hippocampus"] and verify["affine_mri_eq_telencephalon"], \
    "affine mismatch between MRI and labels"
assert len({tuple(v) for v in verify["shapes"].values()}) == 1, "shape mismatch between MRI and labels"
assert hip_vox == 74899, f"hippocampus voxel count {hip_vox} != 74899"
log["niivue_verification"] = verify
print("NiiVue set verified:", json.dumps(verify), flush=True)

# ----------------------------------------------------------------------------
# Helpers for meshes
# ----------------------------------------------------------------------------
def build_mesh(volume_f32, affine, step_size, color_rgba, smooth_iters):
    verts, faces, normals, _ = measure.marching_cubes(
        volume_f32, level=0.5, step_size=step_size)
    verts_mm = nib.affines.apply_affine(affine, verts)
    mesh = trimesh.Trimesh(vertices=verts_mm, faces=faces,
                           vertex_normals=normals, process=False)
    if smooth_iters:
        trimesh.smoothing.filter_taubin(mesh, lamb=0.5, nu=-0.53,
                                        iterations=smooth_iters)
    mesh.visual.vertex_colors = np.tile(
        np.array(color_rgba, dtype=np.uint8), (len(mesh.vertices), 1))
    return mesh

def export_under_budget(mesh, path, volume_f32, affine, color_rgba,
                        smooth_iters, first_step):
    """Export mesh; if GLB >= budget, rebuild at coarser MC step. Returns info."""
    step = first_step
    while True:
        mesh.export(path)
        size = os.path.getsize(path)
        if size < GLB_BUDGET or step >= 3:
            return mesh, step, size
        step += 1
        print(f"  GLB {size} B >= budget at step {step-1}; rebuilding step {step}",
              flush=True)
        mesh = build_mesh(volume_f32, affine, step, color_rgba, smooth_iters)

# ----------------------------------------------------------------------------
# 2. Hippocampus mesh v2 — full-res label, marching cubes step 1, light Taubin
# ----------------------------------------------------------------------------
print("Building hippocampus mesh (full-res, step 1, Taubin x5)...", flush=True)
hip_f32 = hip.astype(np.float32)
mesh = build_mesh(hip_f32, hip_img.affine, step_size=1,
                  color_rgba=[230, 60, 40, 255], smooth_iters=5)
p = os.path.join(OUT, "lion_hippocampus_surface.glb")
mesh, used_step, size = export_under_budget(
    mesh, p, hip_f32, hip_img.affine, [230, 60, 40, 255], 5, first_step=1)
chk = trimesh.load(p, force='mesh')
log["lion_hippocampus_surface.glb"] = dict(
    bytes=size, mc_step_size=used_step, smoothing="Taubin lamb=0.5 nu=-0.53, 5 iterations",
    vertices=int(len(chk.vertices)), faces=int(len(chk.faces)),
    watertight=bool(chk.is_watertight),
    volume_mm3=round(float(chk.volume), 1) if chk.is_watertight else None,
    reload_ok=True)
print("Hippocampus mesh:", log["lion_hippocampus_surface.glb"], flush=True)
del hip_f32

# ----------------------------------------------------------------------------
# 3. Whole-brain mesh v2 — lab Otsu mask at FULL resolution (no downsample)
# ----------------------------------------------------------------------------
print("Building whole-brain mesh (full-res Otsu mask)...", flush=True)
mask = np.load(f"{SRC}/outputs/lion_brainmask_otsu.npy")  # bool, full-res grid
mask_vox = int(mask.sum())
mask_vol = float(mask_vox * 0.3**3 / 1000.0)
mask_f32 = mask.astype(np.float32)
del mask
mesh = build_mesh(mask_f32, mri.affine, step_size=1,
                  color_rgba=[190, 190, 200, 255], smooth_iters=5)
p = os.path.join(OUT, "lion_brain_surface.glb")
mesh, used_step, size = export_under_budget(
    mesh, p, mask_f32, mri.affine, [190, 190, 200, 255], 5, first_step=1)
chk = trimesh.load(p, force='mesh')
log["lion_brain_surface.glb"] = dict(
    bytes=size, mc_step_size=used_step, smoothing="Taubin lamb=0.5 nu=-0.53, 5 iterations",
    mask_voxels=mask_vox, mask_volume_cm3=round(mask_vol, 2),
    vertices=int(len(chk.vertices)), faces=int(len(chk.faces)),
    watertight=bool(chk.is_watertight),
    volume_mm3=round(float(chk.volume), 1) if chk.is_watertight else None,
    reload_ok=True)
print("Brain mesh:", log["lion_brain_surface.glb"], flush=True)
del mask_f32

# ----------------------------------------------------------------------------
# 4. Rhino profile chart — REAL data, cross-checked against paper Table 2
# ----------------------------------------------------------------------------
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = os.path.expanduser(
    "~/workspace/goldmine-hunter/gold/morpho-ct/epmc-rhino5/profiles_all5_complete6.csv")
BONES = ["Humerus", "Radius", "Ulna", "Femur", "Tibia", "Fibula"]
# Table 2, paper.md section 3.3 (complete-6 mean profiles, 4 dp as published)
TABLE2 = {
    "Ceratotherium_simum":      [0.1190, 0.0127, -0.0457, 0.1681, -0.0298, -0.2243],
    "Dicerorhinus_sumatrensis": [0.1353, 0.0053, -0.0538, 0.1723, -0.0259, -0.2332],
    "Diceros_bicornis":         [0.1180, 0.0257, -0.0361, 0.1531, -0.0293, -0.2315],
    "Rhinoceros_sondaicus":     [0.1586, 0.0017, -0.0533, 0.1724, -0.0347, -0.2447],
    "Rhinoceros_unicornis":     [0.1296, -0.0085, -0.0651, 0.1811, -0.0185, -0.2187],
}
df = pd.read_csv(CSV)
means = df.groupby("species")[BONES].mean()
counts = df.groupby("species").size().to_dict()
cross = {}
for sp, ref in TABLE2.items():
    got = means.loc[sp, BONES].to_numpy(dtype=float)
    maxdiff = float(np.max(np.abs(got - np.array(ref))))
    cross[sp] = dict(computed=[round(float(v), 4) for v in got],
                     table2=ref, max_abs_diff=maxdiff, n=int(counts[sp]))
    if maxdiff > 5e-4:
        print(f"CROSS-CHECK FAILED for {sp}: max abs diff {maxdiff}", flush=True)
        sys.exit(1)
log["rhino_crosscheck"] = cross
print("Rhino cross-check PASSED (all species, max abs diff "
      f"{max(c['max_abs_diff'] for c in cross.values()):.2e})", flush=True)

PRETTY = {
    "Ceratotherium_simum": "Ceratotherium simum (white)",
    "Dicerorhinus_sumatrensis": "Dicerorhinus sumatrensis (Sumatran)",
    "Diceros_bicornis": "Diceros bicornis (black)",
    "Rhinoceros_sondaicus": "Rhinoceros sondaicus (Javan)",
    "Rhinoceros_unicornis": "Rhinoceros unicornis (greater one-horned)",
}
ORDER = ["Ceratotherium_simum", "Dicerorhinus_sumatrensis", "Diceros_bicornis",
         "Rhinoceros_sondaicus", "Rhinoceros_unicornis"]
x = np.arange(len(BONES))
# Clean / minimal premium style (site design direction, 2026-11-17): white
# ground, muted ink-navy ramp for the species lines, a single warm amber
# highlight for the forearm band, light gridlines only, no chart junk.
INK = "#16283f"        # ink navy (primary line / title)
MUTED = "#5c6d7f"      # tick / axis text
FAINT = "#e9edf1"      # gridlines
AMBER = "#e19a2f"      # the one warm highlight
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "text.color": INK, "axes.edgecolor": "#c8d0d8",
    "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "svg.fonttype": "none",
})
LINE_COLORS = ["#16283f", "#46617e", "#7d94ab", "#a9bccb", "#546e7a"]
fig, ax = plt.subplots(figsize=(16, 6), dpi=100)
ax.axvspan(0.5, 2.5, color=AMBER, alpha=0.13, zorder=0)
ax.text(1.5, 0.208, "forearm", ha="center", va="top", fontsize=10.5,
        color="#9a7414", style="italic")
ax.axhline(0, color="#c8d0d8", lw=0.9, zorder=1)
for sp, mk, c in zip(ORDER, ["o", "s", "^", "D", "v"], LINE_COLORS):
    ax.plot(x, means.loc[sp, BONES].to_numpy(dtype=float), marker=mk, lw=1.8,
            ms=4.5, color=c, markeredgecolor="white", markeredgewidth=0.7,
            label=f"{PRETTY[sp]}, n = {counts[sp]}")
ax.set_xticks(x)
ax.set_xticklabels([b.lower() for b in BONES], fontsize=11)
ax.tick_params(axis="both", length=0, labelsize=10.5)
ax.set_ylabel("Centred log$_{10}$ centroid size\n(relative to specimen mean)",
              fontsize=11)
ax.set_title("Within-specimen centroid-size profiles of the six long bones",
             fontsize=14.5, color=INK, loc="left", pad=38)
ax.text(0, 1.018, "Five living rhinoceros species — complete-6 specimens, "
        "Mallet et al. (2019) landmark data",
        transform=ax.transAxes, fontsize=11, color=MUTED, va="bottom")
ax.set_ylim(-0.27, 0.22)
ax.grid(axis="y", color=FAINT, lw=0.8, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_linewidth(0.8)
leg = ax.legend(fontsize=10.5, loc="lower left", frameon=False)
for txt in leg.get_texts():
    txt.set_color(MUTED)
fig.tight_layout()
p = os.path.join(OUT, "rhino_profile_chart.png")
fig.savefig(p, dpi=100, facecolor="white")
plt.close(fig)
log["rhino_profile_chart.png"] = dict(bytes=os.path.getsize(p), width_px=1600,
                                      height_px=600)

print(json.dumps(log, indent=1))
with open(os.path.expanduser(
        "~/workspace/github-dashboard/build_brain_assets_v2_log.json"), "w") as f:
    json.dump(log, f, indent=1)
