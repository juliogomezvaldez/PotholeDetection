import os
import shutil
import xml.etree.ElementTree as ET

# Define your classes
classes = ["pothole"]

# Input paths
xml_input_dir = "datasets/archive/annotations"      # Replace with path where XML files are
img_input_dir = "datasets/archive/images"    # Replace with path where images (.jpg) are

# Output paths
labels_output_dir = "datasets/labels/train"   # Replace with output path for YOLO labels
images_output_dir = "datasets/images/train"   # Replace with output path for images

# Create output directories if they don't exist
os.makedirs(labels_output_dir, exist_ok=True)
os.makedirs(images_output_dir, exist_ok=True)

# Conversion function
def convert(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    with open(output_file, "w") as f:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            x_min = int(xmlbox.find('xmin').text)
            x_max = int(xmlbox.find('xmax').text)
            y_min = int(xmlbox.find('ymin').text)
            y_max = int(xmlbox.find('ymax').text)

            x_center = (x_min + x_max) / 2.0 / width
            y_center = (y_min + y_max) / 2.0 / height
            obj_width = (x_max - x_min) / width
            obj_height = (y_max - y_min) / height

            f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {obj_width:.6f} {obj_height:.6f}\n")

# Process all XMLs and move corresponding images
for xml_filename in os.listdir(xml_input_dir):
    if not xml_filename.endswith('.xml'):
        continue
    base_filename = xml_filename.replace('.xml', '')
    xml_path = os.path.join(xml_input_dir, xml_filename)
    label_output_path = os.path.join(labels_output_dir, base_filename + '.txt')
    convert(xml_path, label_output_path)

    # Move corresponding image
    image_filename_jpg = base_filename + '.png'
    image_path = os.path.join(img_input_dir, image_filename_jpg)
    if os.path.exists(image_path):
        shutil.copy(image_path, os.path.join(images_output_dir, image_filename_jpg))
    else:
        print(f"⚠️ Warning: Image file {image_filename_jpg} not found!")

print("✅ Conversion and image moving completed!")
