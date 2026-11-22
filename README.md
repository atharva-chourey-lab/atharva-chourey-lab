# Atharva Chourey Lab

**Auditing the measurements science stopped checking.**

A human–AI research lab: Atharva Chourey, working in sustained collaboration with Lapis, an AI research partner (Muse). Every result below is the product of that collaboration — human questions, judgement and verification; AI search, extraction and audit at a scale neither reaches alone.

Working in neuroanatomy, astronomy, and historical statistics. One programme: take the published measurements everyone cites and nobody re-verifies, and check them against the archives they came from.

## The lab in numbers

- **18 manuscripts published openly** in a single programme — neuroanatomy, comparative morphology, astronomy, history of science, historical statistics, bioacoustics, and conservation — each licensed CC BY 4.0, each with a complete map from every number to its source.
- **343 species** compared across the two great brain archives; **53 of 71** archive labels recovered (the other 18 were empty placeholders).
- **The brain-mass canon disagrees with itself** — across the **1,467 species** shared by the three standard compilations, **30.47%** differ by more than 5%, and only **25%** of sampled values from the most-cited canon trace to an actual measurement.

- **A frozen frog-call archive is filed under dead names** — **146 of 629** species-named recordings (23.2%) in the stranded Fonoteca Zoológica pile no longer carry their filed name, against **1.1%** in a maintained archive run through the same audit; a frozen hand-drawn manatee catalogue of **210 entries** was transcribed and audited against the public record.

- **30 marmoset brains measured twice** — alive and after perfusion fixation — disagree by 21% in the hippocampal formation; across **42 species** with both a skull and a brain measurement, the brain fills a median 92% of the skull, not the assumed 100% (occupancy variation itself is Waugh & Thewissen's 2021 result; the cross-compilation medians and circularity audit are this lab's).
- **First MRI hippocampus measurement for the lion** — 2.02 cm³, against the 4.50 cm³ value the field had cited since 2007.
- **34 historical units** re-quantified for the 1899–1900 famine; **24 received numbers** audited bearer by bearer; **23 standard research questions** graded for whether they can be answered at all.
- **11 headline claims precedent-checked before publication** — 4 held, 4 narrowed, 3 withdrawn. The withdrawals are part of the record, not an embarrassment: the audit applies to the lab first.

## Research

**Two brain archives disagree by a factor of 1.6** — *Neuroanatomy, 2026*
An end-to-end audit of a public comparative-brain archive recovered 53 usable labels of 71 (the rest were empty placeholders) and produced the first MRI hippocampus measurement for the lion: 2.02 cm³, against the 4.50 cm³ histological value cited since 2007. Across 343 paired species, the shrinkage-corrected histological compilation runs ~1.6× above the MRI atlas — a property of the two archives.

Manuscript: [github.com/atharva-chourey-lab/lost-atlas](https://github.com/atharva-chourey-lab/lost-atlas)

**The brain-mass canon is a photocopy chain** — *Comparative neuroanatomy, 2026*
The three compilations treated as the primary record of mammal brain mass — Burger et al. (2019), Smaers et al. (2021), Tsuboi et al. (2018) — were diffed against each other and traced to source under a pre-registration fixed before any download. Of the 1,467 species present in at least two canons, 30.47% disagree by more than 5% on brain mass; of 60 sampled Burger values, only 25.0% terminate in a work that measured a brain — the rest terminate in earlier compilations, five of which supply 82.6% of the canon. Its worst errors trace to mislabelled specimens weighed in 1908 and 1940.

Manuscript: [github.com/atharva-chourey-lab/photocopy-chain](https://github.com/atharva-chourey-lab/photocopy-chain)

**The same brain measures 21% smaller after fixation** — *Neuroanatomy, 2026*
Thirty marmosets in the Brain/MINDS dataset were scanned in vivo and again ex vivo after perfusion fixation — the same brains, the same atlas, the same pipeline — under a test pre-registered before any download. The hippocampal formation reads a median 21.0% smaller in the fixed brain (all 30 pairs negative); total labelled gray matter reads 10.4% smaller (the shipped atlas labels gray matter only — a declared scope). The shift is structure-dependent, not a uniform scale factor. Yoshimaru et al. (2024) first ran this paired comparison at n = 12 and found significant shrinkage (≈ −12% for the hippocampal formation, read from their Fig. 3); this study re-measures it at n = 30 on the public dataset and finds a larger effect — the ~9-point gap between the estimates is an open question.

Manuscript: [github.com/atharva-chourey-lab/marmoset-two-rulers](https://github.com/atharva-chourey-lab/marmoset-two-rulers)

**The brain does not fill the skull — and the rulers disagree by more than the shortfall** — *Neuroanatomy, 2026*
The circularity leads, because it is this audit's own: the largest modern endocast dataset back-calculates skull volume from brain volume for 149 of its species, silently assuming the ~90% occupancy it appears to measure; and a pre-registered second arm joining the Burger canon to the same measured endocasts found that of 129 shared species, 71 (55%) carry the identical number on both sides (Ashwell 2008 and Isler et al. 2008 cited by both datasets) — a naive join of all 129 would have appeared to confirm the identity it was built to test. With those excluded as registered, the second arm gives 58 independent species at median occupancy 0.932, 65.5% outside the band. The first arm's cross-compilation join (42 species) gives median 0.919, only 40.5% inside the 90–100% band fossil quotients assume, and 19.0% above a physically impossible 100% — the field's two brain rulers disagree by more than the shortfall itself.

Prior art, credited: that occupancy varies and is not 100% is Waugh & Thewissen's (2021) established result (33–98% on directly measured pairs; the bowhead their outlier), and this audit builds on their paired table. The cross-compilation statistics and both circularity measurements have no prior found.

Manuscripts: [github.com/atharva-chourey-lab/occupancy-audit](https://github.com/atharva-chourey-lab/occupancy-audit) · [github.com/atharva-chourey-lab/occupancy-second-arm](https://github.com/atharva-chourey-lab/occupancy-second-arm)

**Rainfall did not drive the famine of 1900** — *Historical statistics, 2026*
A famine panel from the 1908 Imperial Gazetteers (34 units; first extracted as an economic panel by Roy, 2014) re-quantifies a contrast the 1901 Census itself reported — princely states −16.2%, British districts −7.5% — and adds the null: correlation with mean rainfall is −0.05. Political boundaries, not weather, carry the signal.

Manuscript: [github.com/atharva-chourey-lab/gazetteers-famine-1900](https://github.com/atharva-chourey-lab/gazetteers-famine-1900)

**Two published estimates for the 1715 eclipse differ by 0.98″** — *Astronomy, 2026*
Re-reducing historical eclipse observations with modern lunar topography: solar radius 959.494 ± 0.044″, consistent with neither Auwers nor the IAU standard. The two canonical reductions disagree on 7 of 9 overlapping eclipses, with five sign flips.

Manuscript: [github.com/atharva-chourey-lab/eclipse-radius](https://github.com/atharva-chourey-lab/eclipse-radius)

**Nalanda's excavated plant cannot hold its received number** — *History of science, 2026*
The attribution itself is old scholarship (Beal, 1884/1911; Deeg, 2018): the 10,000 figure is Huili's, in his biography of Xuanzang, not Xuanzang's own. What this audit adds is the test — a plaque-counted capacity ceiling below 2,000 residents, an endowment cross-check that refutes Huili by his own numbers, and a graded peak of 2,500–4,500, centred near 3,000–3,500 — inside a bearer-by-bearer audit of two dozen received numbers. (The 10,000 is still routinely credited to Xuanzang in exam-prep and popular materials — a persistence documented anecdotally; no textbook survey has been run.)

Manuscript: [github.com/atharva-chourey-lab/received-numbers](https://github.com/atharva-chourey-lab/received-numbers)

**Most questions in Indian historical statistics cannot be answered** — *Methodology, 2026*
The Testability Atlas: of 23 standard questions graded against surviving data, 4 are testable, 11 underpowered, 8 untestable in principle.

Manuscript: [github.com/atharva-chourey-lab/testability-atlas](https://github.com/atharva-chourey-lab/testability-atlas)

**The forearm splits the rhinos** — *Morphology, 2026*
A within-specimen size-allocation profile computed from Mallet et al. (2019)'s open landmark data — a comparison the source study never made — separates all five living rhino species: all 10 pairwise permutation tests significant, the largest split between the black and greater one-horned rhinos (0.0566 log₁₀, p = 0.0014), carried by the relative size of the forearm bones. The dataset was located by the lab's Goldmine Hunter tool.

Manuscript: [github.com/atharva-chourey-lab/rhino-forearm](https://github.com/atharva-chourey-lab/rhino-forearm)

**Dead names in a frozen archive** — *Bioacoustics, 2026*
The stranded Fonoteca Zoológica frog-call pile (1,013 audio files, in no formal archive) was re-identified name by name against the GBIF Backbone Taxonomy: 146 of 629 species-named recordings (23.2%) no longer carry their filed name. The maintained FNJV archive, run through the identical instrument, changed at 1.1% — the dead-name burden of an archive is a property of its filing state, not its era. The dataset was located by the lab's Goldmine Hunter tool.

Manuscript: [github.com/atharva-chourey-lab/fonozoo-reidentification](https://github.com/atharva-chourey-lab/fonozoo-reidentification)

**A frozen sketch catalogue, audited** — *Sirenian conservation, 2026*
The Blue Spring manatee study's hand-drawn scar-sheet catalogue, frozen in April 2013 in a medium the photographic MIPS system does not ingest, was transcribed in full (210 entries) and joined under pre-registration to every public post-2013 record. Public records reach only 21.5% of the catalogue, so the registered fallback governs: a coverage audit and case series (scorecard 2 pass / 3 fail / 1 void), with identities persisting far past the sheet's own drop rules where records exist.

Manuscript: [github.com/atharva-chourey-lab/manatee-scar-sheets](https://github.com/atharva-chourey-lab/manatee-scar-sheets)

**Explore the lion brain interactively:** the [project site](https://atharva-chourey-lab.github.io/atharva-chourey-lab/#brain-atlas) includes a browser viewer for the lion MRI with the hippocampus label overlaid (2.02 cm³, against the 4.50 cm³ value cited since 2007), plus rotatable hippocampus and whole-brain surface meshes. Source atlas: Brain Catalogue — Santin, Herbin & Toro (2016), CC BY-NC 4.0.

## Code & tools

Code behind the papers:

- [brain-archive-audit-code](https://github.com/atharva-chourey-lab/brain-archive-audit-code) — code behind the Lost Atlas brain audit
- [eclipse-reduction-code](https://github.com/atharva-chourey-lab/eclipse-reduction-code) — eclipse solar-radius reduction
- [gazetteers-extraction-code](https://github.com/atharva-chourey-lab/gazetteers-extraction-code) — Gazetteers famine panel extraction
- [testability-atlas-code](https://github.com/atharva-chourey-lab/testability-atlas-code) — Testability Atlas
- [chinese-correlation-spine](https://github.com/atharva-chourey-lab/chinese-correlation-spine) — correlation-spine instrument behind Received Numbers

Discovery tooling:

- [goldmine-hunter](https://github.com/atharva-chourey-lab/goldmine-hunter) — dataset-discovery tooling
- [research-tools](https://github.com/atharva-chourey-lab/research-tools) — relationship-hunting tooling: Pair Hunter, Custody Mapper, Citation Tracer
- [mound-hunter](https://github.com/atharva-chourey-lab/mound-hunter) — DEM mound-detection tooling

Licences: code is MIT-licensed; the manuscripts are CC BY 4.0.

## Method

Pre-registration before extraction · novelty scrub before claiming · blind benchmarks before trusting a pipeline · self-correction on the record.

## Status

All eighteen manuscripts are published in this account's repositories (two of them registered negatives, published in full); the eleven studies above are the featured set. They are manuscripts — not yet peer-reviewed. Public datasets and code will follow in the same repositories.

Site: https://atharva-chourey-lab.github.io/atharva-chourey-lab/
