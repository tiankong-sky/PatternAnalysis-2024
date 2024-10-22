import os
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report
from dataset import get_dataloaders
from train import train_model


def evaluate_model(model, test_loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    report = classification_report(all_labels, all_preds, target_names=["NC", "AD"])
    return report


def main():
    if os.path.exists("recognition/classify_azheimer/AD_NC"):
        data_dir = "recognition/classify_azheimer/AD_NC"
    else:
        data_dir = "/home/groups/comp3710/ADNI/AD_NC/"
    train_loader, test_loader = get_dataloaders(data_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train = True

    if train or not os.path.exists("alzheimer_classifier.pth"):
        model = train_model()
    else:
        model = torch.load("alzheimer_classifier.pth")
    report = evaluate_model(model, test_loader, device)
    print(report)


if __name__ == "__main__":
    main()