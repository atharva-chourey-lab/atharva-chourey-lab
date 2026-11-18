# Dashboard update — instructions (left 2026-11-17 by the consolidation build)

> **Update 2026-11-18 (presentation revision, applied):** the page now opens with the "Twenty-four hours of talking" timeline + method catchline (two session nodes, 16–17 Nov 2026; see LAB-LEDGER.md note for the exact framing), and the Brain Explorer defaults to a Simple view of 37 illustrated animal buttons with all prior controls under an Advanced view toggle. Presentation only — findings, numbers and counts (8 featured / 13 org manuscripts) unchanged.

> **Update 2026-11-17 (evening, site-update build):** the dashboard/site has since been rebuilt around a featured set. The featured page now carries **eight** key findings (the original six plus marmoset-two-rulers at #3 and occupancy-audit at #7) and a dogs entry under Additional findings; the profile README and "lab in numbers" counts on the page read 8 featured manuscripts. The org-wide manuscript count in `lab-ledger.json` / `LAB-LEDGER.md` is **13** (the five history/methodology dossiers of §3 below remain published repos; they are not featured as key-finding cards on the page). The §1 count table below is superseded by the ledger; §§2–4 remain accurate as statements about the org.

**Why this is a note and not an edit:** when the consolidation build inspected this repo, `index.html`, `ASSETS.md` and several `assets/` files carried **uncommitted changes from another session** (`git status`: modified ASSETS.md + lion-brain assets, untracked `clean_*.jpg` images). To avoid clobbering that work, the dashboard itself was **not** touched. Apply the changes below once the in-flight edits are committed. All numbers come from `lab-ledger.json` / `LAB-LEDGER.md` in this directory, computed from the live GitHub org — do not re-derive them by hand.

## 1. Counts to change

| Dashboard stat | Current | New |
|---|---|---|
| Manuscripts | 6 manuscripts | **11 manuscripts** |
| Tools / code repos | (current count) | **7 tools** |
| Total repos | — | **19** (11 papers + 7 tools + this profile repo) |

## 2. New stats to add (the lab's publication pipeline, honestly stated)

- **Publications public:** 11
- **Awaiting peer review:** 11 — every public manuscript is a preprint; **none has been submitted to a journal and none is peer-reviewed.** Do not word this as "under review" anywhere.
- **Submitted to venues:** 0. **Submission packages prepared:** 3 (lost-atlas → *Brain, Behavior and Evolution*; eclipse-radius → *Solar Physics*; testability-atlas → *Historical Methods*), each PREP ONLY.
- **Registered negatives:** 1 (upanishad-gates).
- **Correlation Web anchors:** 133 (47 firm / 74 probable / 12 contested).
- **Campaign cases graded under pre-registration:** 37.

## 3. New paper cards to add (five, added to GitHub 2026-11-17)

1. **bodhidharma-dossier** — *Who was Bodhidharma? A dated-witness stratigraphy and lineage-chart forensics.* Finding: floruit c. 480–530; the famous 527 arrival fails three independent tests; Prajñātāra first attested in 801. https://github.com/atharva-chourey-lab/bodhidharma-dossier
2. **medicine-file** — *The canon travelled west.* Finding: Caraka and Suśruta were translated in Baghdad, never in China; Vāgbhaṭa corroborated c. 550–650 by Yijing (691). https://github.com/atharva-chourey-lab/medicine-file
3. **malabar-mosque** — *An attestation ladder for India's first mosque.* Finding: the 629 date is the tradition's youngest layer, refuted by its own earliest texts; ladder runs 782/783 → 849 → 1124. https://github.com/atharva-chourey-lab/malabar-mosque
4. **thomas-file** — *Thomas in the East.* Finding: Gospel of Thomas c. 70–140; the Gondophares strand plausible–unproven; the Chinese record attests the carrier, never the man. https://github.com/atharva-chourey-lab/thomas-file
5. **upanishad-gates** — *Dating the Bṛhadāraṇyaka Upaniṣad by a linguistic clock: a pre-registered blind-gate failure.* Finding: REGISTERED NEGATIVE — gates failed 0/17 and τ = 0.000; no date was produced; the failure and its diagnosis are the result. https://github.com/atharva-chourey-lab/upanishad-gates

## 4. Do NOT add

- **No separate Nalanda or Correction Campaign cards.** Both already live inside **received-numbers** (paper #4): the Nalanda audit is its §3 flagship and the two campaigns (37 cases) are its second half. A separate card would double-count.
- **No leaderboard, scores, or rankings** — standing lab rule.
- **No "under review" / "submitted" language** for any paper — see §2.

## 5. Optional

- Link **The Correlation Web** compendium page (Muse Library artifact, slug `the-correlation-web`) as a one-page overview of the 2026-11-17 programme.
- The chinese-correlation-spine tool card (if present) can carry the updated anchor count: **133 anchors**.
