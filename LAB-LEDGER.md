# Lab Ledger — Atharva Chourey Lab

*Generated 2026-11-17 by the consolidation build; updated 2026-11-17 (evening) for the marmoset-two-rulers and occupancy-audit manuscripts and the dog-genomics dashboard entry. Machine-readable version: `lab-ledger.json` (same directory). All counts computed from the live GitHub org (`gh repo list atharva-chourey-lab`) and the source files — nothing estimated.*

The Atharva Chourey Lab is an independent research lab, and a human–AI collaboration: Atharva Chourey works with Lapis (Muse), an AI research partner. All results are framed as the collaboration's.

## Status vocabulary (fixed, honest)

- **public** — live on GitHub in the lab's publication format (README publication page, paper.md, SOURCES.md, paper.pdf, CC BY 4.0). **Self-publication is not peer review.**
- **manuscript-in-preparation** — a completed or near-completed manuscript not yet public. Count today: **0** — every completed manuscript is public.
- **registered-negative** — a pre-registered study whose registered success criterion failed, published in full as a negative result.
- **venue_submitted** — true only if a manuscript has actually been submitted to a journal. **It is false for every paper in this ledger.** Three submission packages have been prepared; every one is marked *PREP ONLY — nothing has been submitted, no account created, nothing uploaded.*

## Headline stats

| Statistic | Count |
|---|---|
| Public manuscripts (GitHub) | **13** |
| — of which registered negatives | 1 |
| Manuscripts in preparation (not yet public) | 0 |
| Manuscripts awaiting peer review (public, none submitted to a venue) | **13** |
| Submission packages prepared (not submitted) | 3 |
| Manuscripts actually submitted to a venue | **0** |
| Public tool / code repos | **7** |
| Profile / dashboard repo | 1 |
| **Total repos in the org** | **21** |
| Correlation Web anchors | **133** (47 firm / 74 probable / 12 contested) |
| Campaign cases graded under pre-registration | 37 (+1 skipped under its own pre-registered rule) |
| Interactive 3D viewers | 1 (lion brain) |

## Papers (13, all public, none peer-reviewed)

| # | Repo | Paper | Status | Venue submitted |
|---|---|---|---|---|
| 1 | lost-atlas | Shrinkage-corrected histological compilation values average ~1.6× MRI-atlas values: an audit of a comparative neuroanatomy archive | public | No — package prepared for *Brain, Behavior and Evolution*, PREP ONLY |
| 2 | gazetteers-famine-1900 | Not rainfall: mean rainfall and population loss in the 1899–1900 famine | public | No |
| 3 | eclipse-radius | A re-reduction of historical eclipse observations: solar radius 959.494 ± 0.044″ and a probable sign error in the canonical archive | public | No — package prepared for *Solar Physics*, PREP ONLY |
| 4 | received-numbers | Received numbers: a bearer-by-bearer audit of famous figures in Indian history | public | No |
| 5 | testability-atlas | The Testability Atlas: Which Questions in Indian Historical Statistics Can Surviving Data Decide? | public | No — package prepared for *Historical Methods*, PREP ONLY |
| 6 | rhino-forearm | The Forearm Splits the Rhinos: within-specimen centroid-size profiles separate all five living species | public | No |
| 7 | bodhidharma-dossier | Who was Bodhidharma? A dated-witness stratigraphy and lineage-chart forensics | public (added 2026-11-17) | No |
| 8 | medicine-file | The canon travelled west: dating the Ayurvedic saṃhitās against the Baghdad, Chinese and Tibetan records | public (added 2026-11-17) | No |
| 9 | malabar-mosque | An attestation ladder for India's first mosque: the Cheraman tradition against the dated record | public (added 2026-11-17) | No |
| 10 | thomas-file | Thomas in the East: the Gospel of Thomas, the Gondophares strand, and the limits of the Chinese record | public (added 2026-11-17) | No |
| 11 | upanishad-gates | Dating the Bṛhadāraṇyaka Upaniṣad by a linguistic clock: a pre-registered blind-gate failure | **registered-negative** (also public) | No |
| 12 | marmoset-two-rulers | One Brain, Two Rulers: the hippocampal formation measures 21% smaller after perfusion fixation in the same marmoset brains | public (added 2026-11-17) | No |
| 13 | occupancy-audit | The Brain Does Not Fill the Skull: a 42-species occupancy audit finds ruler chaos, not a constant | public (added 2026-11-17) | No |

### Reconciliation note — Nalanda and the campaigns

There are deliberately **no** `nalanda-capacity` or `correction-campaign` repos. The Nalanda statistical build (49 graded quantities) and both correction campaigns (15 + 22 cases) were already consolidated into **received-numbers** (paper #4) before this build; duplicating them as separate repos would double-count the same results. The five new repos (#7–#11) are the Correlation Web outputs that had no paper home.

## Tools (7, all public)

| Repo | What it is |
|---|---|
| chinese-correlation-spine | The Correlation Web's instrument: 133 graded foreign dated anchors constraining Indian dates; reign-era→CE converter (106 eras); measured composition-to-translation lag model (n = 5 solid, median 186 yrs, PROVISIONAL); circularity guard. MIT code. |
| goldmine-hunter | Finds datasets stranded on project websites that never reached the formal archives. |
| mound-hunter | DEM-based hunt for vanished archaeological mounds in the Narmada corridor. |
| brain-archive-audit-code | Label audit, segmentation and volumetry for the Lost Atlas. |
| eclipse-reduction-code | Historical eclipse re-reduction against LOLA topography. |
| gazetteers-extraction-code | Imperial Gazetteers re-extraction and famine-panel analysis. |
| testability-atlas-code | Testability grading machinery for the Atlas. |

*Note on the spine repo: it was already public (snapshot publish, commit `c5bff11`) before this build. Its tool files (`spine.py`, tests, `data/`) were verified byte-identical to the local working repo's HEAD on 2026-11-17; the local repo's 13-commit working history was deliberately not force-pushed over the published snapshot.*

## Datasets

| Dataset | Records | Where |
|---|---|---|
| Correlation Web anchor database | 133 anchors (53 TAQ / 54 floruit / 25 synchronism / 1 TPQ) | chinese-correlation-spine, `data/anchors.json` |
| Nalanda graded quantities | 49 | `nalanda/numbers.csv` (behind received-numbers §3) |
| Campaign verdict set | 37 graded (+1 skipped, reported) | received-numbers; sources in `campaign/`, `campaign2/` |
| Gazetteers famine panel | 34 units (11 princely states, 23 British districts) | gazetteers-famine-1900 |
| Testability grading grid | 23 questions (4 testable / 11 underpowered / 8 untestable) | testability-atlas |
| Marmoset paired volumes | 30 in-vivo/ex-vivo pairs × 104 labels | behind marmoset-two-rulers; source build in the lab's brain-scan-comparison record |
| Occupancy joined table | 42 species (brain volume × endocranial volume, with ruler pair) | behind occupancy-audit; source build in the lab's brain-scan-comparison record |
| Dog-genomics replication + lifespan join | 1,873-dog breed GWAS set; 125-breed lifespan join | local build (~/workspace/dog-genomics/); dashboard/site entry only — no manuscript repo this pass |

*(The spine's `exports/panel.csv` predates the Medicine merge and carries 117 rows; `anchors.json` at 133 is authoritative.)*

## 3D assets

One interactive viewer on the dashboard: the **lion brain** — structural MRI volume (NIfTI, Zenodo 44855, CC BY-NC 4.0), hippocampus and telencephalon label overlays, and two surface meshes (whole brain, 28,417 verts; hippocampus, 45,393 verts) with OBJ copies and 2D slice/QC fallbacks. Full provenance and licence verdict in `ASSETS.md`.

## Pre-registrations

1. **Bṛhadāraṇyaka dating** — `PREREGISTRATION.md` + Amendments 1–5, committed before any extraction. Gates failed; published as *upanishad-gates*.
2. **Correction Campaign 1** — 15 cases (+ Bodhidharma addendum), verdict classes fixed in advance.
3. **Correction Campaign 2** — scopes A–D declared before grading; scope E (Mahāvīra) by addendum, registered before any E case was graded.
4. **Testability Atlas** — rubric, machinery and anchors registered before grading.
5. **Marmoset paired fixation test** — decide-test thresholds (>5% total, >10% hippocampal) and kill conditions K1–K3 committed before any download; published as *marmoset-two-rulers*.
6. **Occupancy audit** — kill conditions K1/K2 and source-priority rules registered; protocol amended after source inspection, before any join; published as *occupancy-audit*.
7. **Dog genomics** — grading sets and verdict rules committed before any association ran (Hayward 17 QTLs, Plassais markers, McMillan lifespan join).

## Also published

- **The Correlation Web** — a one-page compendium of the 2026-11-17 programme (Muse Library artifact, slug `the-correlation-web`). A presentation artifact, not a manuscript and not a journal submission.
