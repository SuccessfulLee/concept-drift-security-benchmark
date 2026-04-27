import numpy as np
import os
import pickle

# Define the corruption types and severity levels for each task
task_corruptions = {
    0: {'corruptions': ['gaussian_noise'], 'severity': 1},
    1: {'corruptions': ['shot_noise'], 'severity': 1},
    2: {'corruptions': ['motion_blur'], 'severity': 2},
    3: {'corruptions': ['frost'], 'severity': 2},
    4: {'corruptions': ['contrast'], 'severity': 3},
    5: {'corruptions': ['gaussian_noise', 'motion_blur'], 'severity': 3},
    6: {'corruptions': ['shot_noise', 'frost', 'contrast'], 'severity': 4},
    7: {'corruptions': ['gaussian_noise', 'defocus_blur', 'snow', 'brightness'], 'severity': 4},
    8: {'corruptions': ['impulse_noise', 'glass_blur', 'fog', 'elastic_transform'], 'severity': 5},
    9: {'corruptions': ['gaussian_noise', 'motion_blur', 'frost', 'contrast', 'jpeg_compression'], 'severity': 5}
}

# Parameter settings
root_path = './CIFAR-100-C'  # Root directory of the CIFAR-100-C dataset
num_tasks = 10  # Number of tasks
classes_per_task = 10  # Number of classes per task
seed = 42  # Random seed
train_split = 0.7  # Training set ratio

# Create the output directory
output_dir = 'concept_drift_dataset'
os.makedirs(output_dir, exist_ok=True)

# Load labels
labels_path = os.path.join(root_path, 'labels.npy')
if not os.path.exists(labels_path):
    raise FileNotFoundError(f"Label file not found: {labels_path}")
labels = np.load(labels_path)  # Shape: (50000,)

# Set the random seed
np.random.seed(seed)

# Generate the dataset for each task
for task_id in range(num_tasks):
    print(f"Processing task {task_id}...")

    # Class range of the current task
    start_class = task_id * classes_per_task
    end_class = start_class + classes_per_task
    task_classes = np.arange(start_class, end_class)
    print(f"Task {task_id} classes: {task_classes}")

    # Corruption types and severity level of the current task
    task_config = task_corruptions[task_id]
    corruptions = task_config['corruptions']
    severity = task_config['severity']
    print(f"Corruption types: {corruptions}, severity: {severity}")

    # Compute the index range for the selected severity level
    start_idx = (severity - 1) * 10000
    end_idx = severity * 10000

    # Load and combine corrupted data
    if len(corruptions) == 1:
        # Single corruption type
        corruption_file = os.path.join(root_path, f"{corruptions[0]}.npy")
        if not os.path.exists(corruption_file):
            raise FileNotFoundError(f"Corruption file not found: {corruption_file}")
        data = np.load(corruption_file)[start_idx:end_idx]  # Shape: (10000, 32, 32, 3)
    else:
        # Multiple corruption types combined by averaging
        base_file = os.path.join(root_path, f"{corruptions[0]}.npy")
        if not os.path.exists(base_file):
            raise FileNotFoundError(f"Corruption file not found: {base_file}")
        data = np.load(base_file)[start_idx:end_idx].astype(np.float32)
        for corruption in corruptions[1:]:
            corruption_file = os.path.join(root_path, f"{corruption}.npy")
            if not os.path.exists(corruption_file):
                raise FileNotFoundError(f"Corruption file not found: {corruption_file}")
            additional_data = np.load(corruption_file)[start_idx:end_idx].astype(np.float32)
            data = (data + additional_data) / 2
        data = data.astype(np.uint8)

    # Get the labels corresponding to the selected severity level
    task_labels = labels[start_idx:end_idx]  # Shape: (10000,)

    # Filter the classes of the current task
    task_indices = np.isin(task_labels, task_classes)
    task_data = data[task_indices]  # Shape: (num_samples, 32, 32, 3)
    task_labels = task_labels[task_indices]  # Shape: (num_samples,)
    print(f"Task {task_id} total samples: {len(task_data)}")

    # Train/test split
    train_indices = []
    test_indices = []
    for cls in task_classes:
        cls_indices = np.where(task_labels == cls)[0]
        if len(cls_indices) == 0:
            print(f"Warning: class {cls} has no samples")
            continue
        np.random.shuffle(cls_indices)
        split_idx = int(train_split * len(cls_indices))
        train_indices.extend(cls_indices[:split_idx])
        test_indices.extend(cls_indices[split_idx:])

    # Extract training and test data
    train_data = task_data[train_indices]
    train_labels = task_labels[train_indices]
    test_data = task_data[test_indices]
    test_labels = task_labels[test_indices]
    print(f"Training set: {len(train_data)} samples, test set: {len(test_data)} samples")

    # Flatten image data to match the CIFAR-100 format
    train_data_flat = train_data.reshape(len(train_data), -1)  # Shape: (num_train, 3072)
    test_data_flat = test_data.reshape(len(test_data), -1)  # Shape: (num_test, 3072)

    # Create dictionaries in CIFAR-100 format
    train_dict = {
        'data': train_data_flat,
        'fine_labels': train_labels.tolist()
    }
    test_dict = {
        'data': test_data_flat,
        'fine_labels': test_labels.tolist()
    }

    # Save as pickle files
    train_file = os.path.join(output_dir, f'task_{task_id}_train')
    test_file = os.path.join(output_dir, f'task_{task_id}_test')
    with open(train_file, 'wb') as f:
        pickle.dump(train_dict, f)
    with open(test_file, 'wb') as f:
        pickle.dump(test_dict, f)

    print(f"Task {task_id} data saved: {train_file}, {test_file}")

# Optional: generate the meta file by reusing the CIFAR-100 class names
meta_dict = {
    'fine_label_names': [
        'apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle', 'bicycle', 'bottle',
        'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel', 'can', 'castle', 'caterpillar', 'cattle',
        'chair', 'chimpanzee', 'clock', 'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur',
        'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster', 'house', 'kangaroo', 'keyboard',
        'lamp', 'lawn_mower', 'leopard', 'lion', 'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain',
        'mouse', 'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear', 'pickup_truck', 'pine_tree',
        'plain', 'plate', 'poppy', 'porcupine', 'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket',
        'rose', 'sea', 'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail', 'snake', 'spider',
        'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table', 'tank', 'telephone', 'television', 'tiger',
        'tractor',
        'train', 'trout', 'tulip', 'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman', 'worm'
    ]
}
meta_file = os.path.join(output_dir, 'meta')
with open(meta_file, 'wb') as f:
    pickle.dump(meta_dict, f)
print(f"Meta file has been saved to: {meta_file}")

print("Dataset construction completed.")