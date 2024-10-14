import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class AlzheimerDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.image_paths = []
        self.labels = []
        self.transform = transform
        categories = ['NC', 'AD']  # Two categories

        for category in categories:
            class_num = categories.index(category)  # Labels (NC: 0, AD: 1)
            path = os.path.join(data_dir, category)

            # Iterate through images in the category folder
            for img_name in os.listdir(path):
                if img_name.endswith(".jpeg") or img_name.endswith(".jpg"):
                    img_path = os.path.join(path, img_name)
                    self.image_paths.append(img_path)
                    self.labels.append(class_num)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]

        # Load as grayscale image (L mode indicates grayscale)
        image = Image.open(img_path).convert("L")

        if self.transform:
            image = self.transform(image)

        return image, label

def get_datasets(train_dir, test_dir, transform):
    train_dataset = AlzheimerDataset(train_dir, transform=transform)
    test_dataset = AlzheimerDataset(test_dir, transform=transform)
    return train_dataset, test_dataset

def get_dataloaders(train_dataset, test_dataset, batch_size=32):
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader
