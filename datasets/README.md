# Pothole Dataset Structure

This folder contains the dataset for training and validating the pothole detection model.

## Structure:
- `images/train/` : Training images
- `images/val/` : Validation images
- `labels/train/` : YOLO format labels for training images
- `labels/val/` : YOLO format labels for validation images

## Annotation Format (YOLO):
Each `.txt` label file contains:
```
<class_id> <x_center> <y_center> <width> <height>
```
- `class_id`: Class index (0 = pothole)
- `x_center`, `y_center`: Normalized center of bounding box (0 to 1)
- `width`, `height`: Normalized width and height (0 to 1)

## Example:
- Image: `example_image.jpg`
- Label: `example_label.txt`
```
0 0.502 0.600 0.150 0.200
```
Meaning: Detected pothole centered at (50.2%, 60.0%) with 15% width and 20% height of the image.

## How to Use:
1. Place your own pothole images into `images/train/` and `images/val/` folders.
2. Create corresponding `.txt` files with the annotation format shown above.
3. Update `potholes.yaml` if needed.
4. Train the model with:
   ```
   yolo detect train data=datasets/potholes/potholes.yaml model=yolov9s.pt epochs=50 imgsz=640
   ```

Author: Julio Gomez
