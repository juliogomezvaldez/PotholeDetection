import os
import random
import shutil

# Paths
images_dir = "path/to/all_images"   # Path where all images are
labels_dir = "path/to/all_labels"   # Path where all labels are
train_images_dir = "path/to/images/train"
val_images_dir = "path/to/images/val"
test_images_dir = "path/to/images/test"
train_labels_dir = "path/to/labels/train"
val_labels_dir = "path/to/labels/val"
test_labels_dir = "path/to/labels/test"

# Split ratios
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Create target directories if they don't exist
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(test_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)
os.makedirs(test_labels_dir, exist_ok=True)

# List all images
images = [img for img in os.listdir(images_dir) if img.endswith(('.jpg', '.jpeg', '.png'))]

# Shuffle images randomly
random.shuffle(images)

# Split indices
total_images = len(images)
train_end = int(total_images * train_ratio)
val_end = train_end + int(total_images * val_ratio)

train_images = images[:train_end]
val_images = images[train_end:val_end]
test_images = images[val_end:]

# Copy function
def copy_files(file_list, src_img_dir, src_lbl_dir, dest_img_dir, dest_lbl_dir):
    for img_file in file_list:
        label_file = img_file.rsplit('.', 1)[0] + '.txt'
        
        # Copy image
        shutil.copy(os.path.join(src_img_dir, img_file), os.path.join(dest_img_dir, img_file))
        
        # Copy corresponding label
        if os.path.exists(os.path.join(src_lbl_dir, label_file)):
            shutil.copy(os.path.join(src_lbl_dir, label_file), os.path.join(dest_lbl_dir, label_file))
        else:
            print(f"⚠️ Warning: Label not found for {img_file}")

# Copy train, val, and test files
copy_files(train_images, images_dir, labels_dir, train_images_dir, train_labels_dir)
copy_files(val_images, images_dir, labels_dir, val_images_dir, val_labels_dir)
copy_files(test_images, images_dir, labels_dir, test_images_dir, test_labels_dir)

print("✅ Dataset 70/20/10 split completed!")
print(f"Training images: {len(train_images)}, Validation images: {len(val_images)}, Testing images: {len(test_images)}")
