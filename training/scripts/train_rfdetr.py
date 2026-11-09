"""Fine-tune Community Fish Detector RF-DETR Small on DIGI4ECO.

Training configuration used for the ClipSift DIGI4ECO pilot:
- RF-DETR 1.12.0
- Input resolution: 512
- Epochs: 5
- Batch size: 2
- Gradient accumulation: 4
- Learning rate: 1e-5
- Single class: Fish

Requires an NVIDIA CUDA GPU and rfdetr[train].
"""

import argparse
from pathlib import Path

import torch
from rfdetr import RFDETRSmall


def main():
    parser = argparse.ArgumentParser(
        description="Fine-tune RF-DETR Small on DIGI4ECO"
    )

    parser.add_argument(
        "--dataset-dir",
        type=Path,
        required=True,
        help="COCO dataset folder containing train, valid and test"
    )

    parser.add_argument(
        "--pretrain-weights",
        type=Path,
        required=True,
        help="Original pretrained Community Fish Detector checkpoint"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Where training checkpoints will be saved"
    )

    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=2)

    args = parser.parse_args()

    if not args.dataset_dir.is_dir():
        parser.error("Dataset directory does not exist")

    for split in ("train", "valid", "test"):
        annotations = (
            args.dataset_dir / split / "_annotations.coco.json"
        )
        if not annotations.is_file():
            parser.error(
                f"Missing COCO annotations: {annotations}"
            )

    if not args.pretrain_weights.is_file():
        parser.error("Pretrained checkpoint does not exist")

    if not torch.cuda.is_available():
        parser.error(
            "CUDA GPU not available. Use a GPU-enabled environment."
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Dataset:", args.dataset_dir)
    print("Pretrained weights:", args.pretrain_weights)
    print("Output:", args.output_dir)
    print("GPU:", torch.cuda.get_device_name(0))

    model = RFDETRSmall(
        pretrain_weights=str(args.pretrain_weights),
        num_classes=1,
        resolution=512,
        device="cuda"
    )

    model.train(
        dataset_dir=str(args.dataset_dir),
        output_dir=str(args.output_dir),
        epochs=args.epochs,
        batch_size=args.batch_size,
        eval_batch_size=1,
        grad_accum_steps=4,
        lr=1e-5,
        lr_encoder=1e-5,
        checkpoint_interval=1,
        run_test=False
    )

    print("Training completed.")


if __name__ == "__main__":
    main()
