"""Convert DIGI4ECO CVAT video tracking XML into COCO detection splits.

Dependencies: opencv-python (cv2); Python standard library.
Original source files are read-only. Frame sampling is deterministic.
"""
import argparse
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import cv2

# Whole-video split: avoid training and validation on adjacent frames.
# SmartBay1 and SmartBay2 are different sequences at the same general site;
# OBSEA is reserved as a separate-site final test.
SPLITS = {
    "train": [("Ancona", 10), ("SmartBay2", 10)],
    "valid": [("SmartBay1", 20)],
    "test": [("OBSEA", 3)],
}


def parse_boxes(xml_path):
    root = ET.parse(xml_path).getroot()
    expected = int(root.findtext("./meta/job/size", default="0"))
    boxes_by_frame = defaultdict(list)
    for track in root.findall(".//track"):
        if track.get("label", "").lower() != "fish":
            continue
        track_id = int(track.get("id", -1))
        for box in track.findall("box"):
            if box.get("outside") == "1":
                continue
            frame_index = int(box.get("frame"))
            boxes_by_frame[frame_index].append({
                "xyxy": [float(box.get(k)) for k in ("xtl", "ytl", "xbr", "ybr")],
                "track_id": track_id,
                "keyframe": int(box.get("keyframe", "0")),
                "occluded": int(box.get("occluded", "0")),
            })
    if not expected:
        expected = max(boxes_by_frame, default=-1) + 1
    return expected, boxes_by_frame


def build(root_path):
    original = root_path / "downloads"
    output = root_path / "dataset_coco"
    for split, sequences in SPLITS.items():
        dest = output / split
        dest.mkdir(parents=True, exist_ok=True)
        coco = {
            "info": {"description": "DIGI4ECO fish detection pilot", "version": "1.0"},
            "licenses": [{"id": 1, "name": "CC BY 4.0", "url": "https://creativecommons.org/licenses/by/4.0/"}],
            "categories": [{"id": 1, "name": "Fish", "supercategory": "animal"}],
            "images": [], "annotations": [],
        }
        image_id = 1
        annotation_id = 1
        for name, stride in sequences:
            video_path = original / name / "video.mp4"
            xml_path = original / name / "annotations.xml"
            if not video_path.is_file() or not xml_path.is_file():
                raise FileNotFoundError(f"Missing video or annotations for {name}")
            expected, boxes_by_frame = parse_boxes(xml_path)
            capture = cv2.VideoCapture(str(video_path))
            if not capture.isOpened():
                raise RuntimeError(f"Cannot open {video_path}")
            saved = 0
            skipped_boxes = 0
            for idx in range(expected):
                # Sequential decoding avoids inaccurate random seeking in MP4 videos.
                if not capture.grab():
                    print(f"WARNING {name}: video ended at frame {idx} (XML says {expected}).")
                    break
                if idx % stride:
                    continue
                ok, image = capture.retrieve()
                if not ok or image is None:
                    print(f"WARNING {name}: cannot decode selected frame {idx}")
                    continue
                h, w = image.shape[:2]
                filename = f"{name}_frame_{idx:06d}.jpg"
                if not cv2.imwrite(str(dest / filename), image, [cv2.IMWRITE_JPEG_QUALITY, 90]):
                    raise RuntimeError(f"Failed writing {filename}")
                coco["images"].append({
                    "id": image_id, "file_name": filename,
                    "width": w, "height": h, "license": 1,
                })
                for box in boxes_by_frame.get(idx, []):
                    x1, y1, x2, y2 = box["xyxy"]
                    x1 = max(0.0, min(float(w), x1))
                    x2 = max(0.0, min(float(w), x2))
                    y1 = max(0.0, min(float(h), y1))
                    y2 = max(0.0, min(float(h), y2))
                    bw, bh = x2 - x1, y2 - y1
                    if bw < 2 or bh < 2:
                        skipped_boxes += 1
                        continue
                    coco["annotations"].append({
                        "id": annotation_id, "image_id": image_id, "category_id": 1,
                        "bbox": [round(x1, 2), round(y1, 2), round(bw, 2), round(bh, 2)],
                        "area": round(bw * bh, 2), "iscrowd": 0,
                        "track_id": box["track_id"],
                        "keyframe": box["keyframe"],
                        "occluded": box["occluded"],
                    })
                    annotation_id += 1
                saved += 1
                image_id += 1
            capture.release()
            print(f"{split:5} | {name:10} | {saved:4} images | skipped boxes: {skipped_boxes}", flush=True)
        json_path = dest / "_annotations.coco.json"
        json_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")
        print(f"{split.upper():5} TOTAL: {len(coco['images'])} images, "
              f"{len(coco['annotations'])} fish boxes -> {json_path}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True, help="Path to dataset workspace")
    args = parser.parse_args()
    build(args.root)
