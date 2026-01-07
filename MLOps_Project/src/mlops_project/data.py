from pathlib import Path
from torchvision import datasets
import torch
import typer


def normalize(train_images: torch.Tensor, test_images: torch.Tensor):
    mean = train_images.mean()
    std = train_images.std()
    return (train_images - mean) / std, (test_images - mean) / std


def preprocess_data(raw_dir: str, processed_dir: str) -> None:
    """
    Download Fashion-MNIST, normalize it, and save tensors.
    """

    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Download dataset
    train = datasets.FashionMNIST(
        root=raw_dir,
        train=True,
        download=True,
    )
    test = datasets.FashionMNIST(
        root=raw_dir,
        train=False,
        download=True,
    )

    # Extract tensors
    train_images = train.data.unsqueeze(1).float()
    train_target = train.targets.long()
    test_images = test.data.unsqueeze(1).float()
    test_target = test.targets.long()

    # Normalize
    train_images, test_images = normalize(train_images, test_images)

    # Save processed data
    torch.save(train_images, processed_dir / "train_images.pt")
    torch.save(train_target, processed_dir / "train_target.pt")
    torch.save(test_images, processed_dir / "test_images.pt")
    torch.save(test_target, processed_dir / "test_target.pt")

    print("✔ Fashion-MNIST downloaded and preprocessed successfully")


def corrupt_mnist() -> tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """Return train and test datasets for corrupt MNIST."""
    train_images = torch.load("data/processed/train_images.pt")
    train_target = torch.load("data/processed/train_target.pt")
    test_images = torch.load("data/processed/test_images.pt")
    test_target = torch.load("data/processed/test_target.pt")

    train_set = torch.utils.data.TensorDataset(train_images, train_target)
    test_set = torch.utils.data.TensorDataset(test_images, test_target)
    return train_set, test_set


if __name__ == "__main__":
    typer.run(preprocess_data)
