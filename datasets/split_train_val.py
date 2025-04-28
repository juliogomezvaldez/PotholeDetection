import os
import random
import shutil

# Paths
images_dir = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/all-images"
labels_dir = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/all-labels"

train_images_dir = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/images/train"
val_images_dir = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/images/val"

train_labels_dir = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/labels/train"
val_labels_dir = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/labels/val"


# Parameters
split_ratio = 0.8  # 80% train, 20% val

# Create target directories if they don't exist
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# List all images
images = [img for img in os.listdir(images_dir) if img.endswith(('.jpg', '.jpeg', '.png'))]

# Shuffle images randomly
random.shuffle(images)

# Split
split_idx = int(len(images) * split_ratio)
train_images = images[:split_idx]
val_images = images[split_idx:]

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

# Copy train files
copy_files(train_images, images_dir, labels_dir, train_images_dir, train_labels_dir)

# Copy val files
copy_files(val_images, images_dir, labels_dir, val_images_dir, val_labels_dir)

print("✅ Dataset split completed!")
print(f"Training images: {len(train_images)}, Validation images: {len(val_images)}")
