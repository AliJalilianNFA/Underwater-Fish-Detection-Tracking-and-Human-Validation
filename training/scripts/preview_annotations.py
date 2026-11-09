import argparse
from pathlib import Path
import cv2
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True,
                    help="Path to dataset workspace")
args = parser.parse_args()

root = args.root
folder = root / "downloads" / "Ancona"
output = root / "results" / "annotation_preview"
output.mkdir(parents=True, exist_ok=True)

frame_number = 100

tree = ET.parse(folder / "annotations.xml")

cap = cv2.VideoCapture(str(folder / "video.mp4"))
if not cap.isOpened():
    raise RuntimeError("Cannot open video")

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ok, frame = cap.read()
cap.release()

if not ok:
    raise RuntimeError("Cannot read frame")

cv2.imwrite(str(output / "ancona_original.jpg"), frame)

counts = {"manual": 0, "interpolated": 0, "occluded": 0}

for track in tree.findall(".//track"):
    track_id = track.get("id")

    for box in track.findall("box"):
        if int(box.get("frame")) != frame_number:
            continue

        if box.get("outside") == "1":
            continue

        x1 = int(float(box.get("xtl")))
        y1 = int(float(box.get("ytl")))
        x2 = int(float(box.get("xbr")))
        y2 = int(float(box.get("ybr")))

        if box.get("occluded") == "1":
            color = (0, 0, 255)
            counts["occluded"] += 1
        elif box.get("keyframe") == "1":
            color = (0, 255, 0)
            counts["manual"] += 1
        else:
            color = (0, 255, 255)
            counts["interpolated"] += 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame, str(track_id), (x1, max(15, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
        )

image_path = output / "ancona_annotated.jpg"
if not cv2.imwrite(str(image_path), frame):
    raise RuntimeError("Could not save annotated image")

print("Frame:", frame_number)
print("Image size:", frame.shape[1], "x", frame.shape[0])
print("Annotations:", counts)
print("Total visible boxes:", sum(counts.values()))
print("Saved:", image_path)
