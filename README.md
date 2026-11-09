# Underwater Fish Detection, Tracking and Human Validation

An experimental AI-assisted system for detecting and tracking fish in underwater videos, with human review of model predictions.

Developed as part of the ClipSift work at RBC HubHacks 2026, with further work on RF-DETR fine-tuning, tiled inference, tracking and validation.

## What This Project Does

Underwater videos can be difficult to analyze because fish may be small, move quickly, overlap, or blend into the background.

This project combines:

- Fish detection using a fine-tuned RF-DETR model
- Tiled inference for high-resolution underwater footage
- Multi-frame object tracking with ByteTrack
- Evidence generation for candidate detections
- Human validation of fish and non-fish predictions
- A local web interface for video analysis and review
- Experiment documentation and evaluation results

The system is not a validated fully automatic fish-counting solution. Human reviewers remain responsible for final decisions.

## Workflow

Underwater Video
    |
    v
RF-DETR Detection
    |
    v
ByteTrack Tracking
    |
    v
Candidate Evidence
    |
    v
Human Review
    |
    v
Results and Reporting

## Project Structure

- `webapp/` - Local ClipSift V6 application, API and interface
- `experiments/digi4eco-finetuned/` - Experimental detector and comparison tools
- `training/scripts/` - Dataset preparation, annotation preview and fine-tuning scripts

## Web Application

The web application provides four main sections:

1. Videos - Select and analyze a local video
2. Subsamples - Inspect detection and tracking evidence
3. Human Review - Label fish, equipment, background and uncertain candidates
4. Results - Review validation decisions and outputs

### Local Setup

Create a Python virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r webapp\requirements.txt
.\.venv\Scripts\python.exe -m pip install -r experiments\digi4eco-finetuned\requirements.txt
```

Compatibility depends on the Python and RF-DETR versions. The experimental checkpoint was successfully tested locally using RF-DETR 1.11.2.

Download or obtain an authorized copy of the trained checkpoint separately.

Set the model path and start the application:

```powershell
$env:CLIPSIFT_MODEL_PATH = "C:\path\to\digi4eco_best.pth"

cd webapp

python -m uvicorn app.local_api:app --host 127.0.0.1 --port 8770
```

Open:

http://127.0.0.1:8770/videos

The video-analysis workflow uses local file paths. It is not a hosted web service.

## Model Development

Base model: Community Fish Detector, RF-DETR Small.

The model was fine-tuned on DIGI4ECO underwater fish annotations using PyTorch and an NVIDIA Tesla T4 GPU.

Pilot training configuration:

- 331 training images
- 120 validation images
- 50 test images
- Five epochs
- 512-pixel input resolution
- Single detection class: Fish

See `training/scripts/train_rfdetr.py` for the training configuration.

## Evaluation

Results on the DIGI4ECO OBSEA test set:

| Metric | Original | Fine-tuned |
|---|---:|---:|
| mAP@50 | 49.82% | 55.87% |
| mAP@50:95 | 18.15% | 27.49% |
| Precision | 66.24% | 73.27% |
| Recall | 45.22% | 48.26% |

These measurements apply to the OBSEA test set, not to verified fish-counting accuracy on Coastal Action footage.

Performance varied significantly across underwater environments.

For details, see:

[Experimental Results](experiments/digi4eco-finetuned/docs/EXPERIMENT_RESULTS.md)

[Model Card](experiments/digi4eco-finetuned/docs/MODEL_CARD.md)

## Training Data

Dataset: DIGI4ECO Underwater Fish Tracking Dataset.

DOI: https://doi.org/10.5281/zenodo.20701225

The dataset was converted from CVAT tracking annotations into COCO detection data.

Dataset files are not included in this repository. Check the source dataset's license and attribution requirements before reuse.

## Model Weights

The fine-tuned model checkpoint is approximately 121 MB and is not included in the Git repository.

The original pretrained model must also be obtained from an authorized source.

Check model licenses and redistribution rights before sharing pretrained or fine-tuned weights.

## Limitations

- Fish detections can include false positives.
- Small, overlapping and low-visibility fish may be missed.
- Tracking can fragment or duplicate fish identities.
- More detection boxes do not necessarily mean more fish.
- Coastal Action counting accuracy has not been established.
- Human review is required.
- Full training reproducibility depends on the original data, model weights and compatible software versions.

## Project Background and Credits

This work originated from ClipSift, developed by the Stride Analytics team during RBC HubHacks 2026 for the Coastal Action challenge.

The original project involved contributions from multiple team members. This repository consolidates the experimental RF-DETR development, training scripts, tracking workflow and local review application for continued development.

Original team project:
https://github.com/A00425511/clipsift

## Status

Experimental research prototype.

The local web application and fine-tuned checkpoint have been tested successfully. Further validation is needed before operational deployment.
