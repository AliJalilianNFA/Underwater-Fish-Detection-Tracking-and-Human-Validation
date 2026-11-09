# ClipSift — Clean Evidence Patch (local review)

## Changes
- Rebuilds one **clean source-video crop** per candidate, without yellow overlays.
- Adds one **full original frame**, highlighting only that candidate's bounding box.
- Adds both images to Human Review; includes source frame index and observation time.
- Leaves RF-DETR, tracking, protocol, AI JSON, and review decisions unchanged.

## Install (stop uvicorn first)

Extract the ZIP. Replace only these three files in the tested Release Candidate:
- `scripts/build_review_queue_v2.py`
- `app/local_api.py`
- `app/demo.html`

Keep backups of the three files before replacing.

## Rebuild evidence from existing run (NO MODEL INFERENCE)

```powershell
cd F:\SMU\ClipSift_Release_Test\ClipSift_Source
F:\SMU\ClipSift_GitHub\.venv\Scripts\python.exe scripts\build_review_queue_v2.py outputs\release_test\subsamples_v6.json
```

The ORIGINAL video path stored in `subsamples_v6.json` must exist on the current machine.
The builder will **not** use the already-overlaid `subsample_001_context.mp4`.

Restart server on 8766, open `/review?run=release_test`, then use `Ctrl+F5`.

Human review decisions reside in `outputs/release_test/review_v2/review_decisions.json` and are not modified. Existing CSV is updated with new evidence paths. Original output data remains unchanged.

**Legacy note:** old output runs with missing original videos cannot produce clean images; restore the original video or re-run analysis after reconnecting the source. The builder fails without overwriting the CSV in that case.

## Preview logic
The clean crop is saved to `review_v2/evidence_crops/`; the original full frame with one yellow rectangle is saved to `review_v2/evidence_full_frames/`.
No automatic fish counts are generated. Track IDs are not fish counts.
