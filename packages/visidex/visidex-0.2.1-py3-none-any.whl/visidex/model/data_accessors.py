from torchvision.transforms import transforms, InterpolationMode
import torch,torchvision, math, os, glob
import numpy as np
from PIL import Image
from visidex.utils import download_file, extract_zip

def read_dataload_flower(img_size,data_path='./datasets',batch_size=60):
    transform2 = transforms.Compose([
        transforms.Resize((img_size,img_size), interpolation=InterpolationMode.BICUBIC),
        transforms.Grayscale(),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])

    trainset = torchvision.datasets.Flowers102(root=data_path, split='train',
                                            download=True, transform=transform2)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                            shuffle=False, num_workers=1)

    testset = torchvision.datasets.Flowers102(root=data_path, split='test',
                                            download=True, transform=transform2)
    num_datapoints_to_keep = 6072
    indices_to_keep = torch.randperm(num_datapoints_to_keep)[:num_datapoints_to_keep]
    reduced_testset = torch.utils.data.Subset(testset, indices_to_keep)
    print(len(reduced_testset))
    testloader = torch.utils.data.DataLoader(reduced_testset, batch_size=batch_size,
                                            shuffle=False, num_workers=1)

    return trainloader,testloader

def read_dataload_fibers(img_size,data_path='./datasets/',batch_size=44,train_percent = 0.1):
    transform2 = transforms.Compose([
        transforms.Resize((img_size,img_size), interpolation=InterpolationMode.BICUBIC),
        transforms.Grayscale(),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])

    url ="https://github.com/binarycode11/visidex/raw/refs/heads/main/data/dataset/fibers.zip"
    local_zip = os.path.join(data_path, "fibers.zip")
    dataset_dir = os.path.join(data_path, "fibers/")

    download_file(url, local_zip)
    extract_zip(local_zip, data_path)

    trainset = FibersDataset(transform=transform2, train=True, path=dataset_dir, limit_train=train_percent)
    testset = FibersDataset(transform=transform2, train=False, path=dataset_dir, limit_train=train_percent)
    print(len(testset))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                shuffle=True, num_workers=2)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                                shuffle=False, num_workers=2)
    return trainloader,testloader

def read_dataload_woods(img_size,data_path='./datasets/',batch_size=31,train_percent = 0.07):
    transform2 = transforms.Compose([
        transforms.Resize((img_size,img_size), interpolation=InterpolationMode.BICUBIC),
        transforms.Grayscale(),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])

    url ="https://github.com/binarycode11/visidex/raw/refs/heads/main/data/dataset/wood_dataset.zip"
    local_zip = os.path.join(data_path, "wood_dataset.zip")
    dataset_dir = os.path.join(data_path, "wood_dataset/")

    download_file(url, local_zip)
    extract_zip(local_zip, data_path)

    trainset = WoodsDataset(transform=transform2, train=True, path=dataset_dir, limit_train=train_percent)
    testset = WoodsDataset(transform=transform2, train=False, path=dataset_dir, limit_train=train_percent)

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                            shuffle=False, num_workers=1)
    num_datapoints_to_keep = 7920
    indices_to_keep = torch.randperm(num_datapoints_to_keep)[:num_datapoints_to_keep]
    reduced_testset = torch.utils.data.Subset(testset, indices_to_keep)
    print(len(reduced_testset))
    testloader = torch.utils.data.DataLoader(reduced_testset, batch_size=batch_size,
                                            shuffle=False, num_workers=1)

    return trainloader,testloader


class FibersDataset(torch.utils.data.Dataset):
    """Fibers dataset. to train neural net"""

    def __init__(self, transform=None, train=True, path='./data/fibers/', limit_train=0.5):
        self.transform = transform
        self.data = glob.glob('{}*.jpg'.format(path))
        limit_train = int(len(self.data) * limit_train)
        self.image_list = []
        if train:
            self.data = self.data[:limit_train]
        else:
            self.data = self.data[limit_train:]
        print(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        filename = self.data[idx]
        img = Image.open(filename)
        img_t = self.transform(img)
        return img_t, ' rrr '


class WoodsDataset(torch.utils.data.Dataset):
    """Fibers dataset. to train neural net"""

    def __init__(self, transform=None, train=True, path='./data/wood/', limit_train=0.5):
        np.random.seed(0)
        self.transform = transform
        # self.data = np.array(sorted(glob.glob('{}*.jpg'.format(path))))
        self.data = np.array(sorted(glob.glob('{}**/*.jpg'.format(path), recursive=True)))

        limit_train = int(len(self.data) * limit_train)
        indices = np.random.permutation(len(self.data))

        training_idx, test_idx = indices[:limit_train], indices[limit_train:]

        self.image_list = []
        if train:
            self.data = self.data[training_idx]
        else:
            self.data = self.data[test_idx]
        print('train ' + str(train), ' ', len(self.data))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        filename = self.data[idx]
        img = Image.open(filename)
        img_t = self.transform(img)
        return img_t, 'wood'