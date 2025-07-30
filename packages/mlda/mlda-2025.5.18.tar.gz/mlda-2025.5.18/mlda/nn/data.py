import torch
import lightning as L
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import numpy as np

class Dataset(L.LightningDataModule):
    def __init__(self, obs=None, prior_da=None, target_da=None):
        super().__init__()
        self.obs = obs
        self.prior_da = prior_da
        self.target_da = target_da

        # c
        self.prior_ens = torch.tensor(self.prior_da.values, dtype=torch.float32)
        self.obs_lats = torch.tensor(self.obs.df['lat'].values, dtype=torch.float32)
        self.obs_lons = torch.tensor(self.obs.df['lon'].values, dtype=torch.float32)
        self.obs_Rs = torch.tensor(self.obs.df['R'].values, dtype=torch.float32)


    def setup(self, stage=None, train_frac=0.7, val_frac=0.1, test_frac=0.2, batch_size=10, num_workers=4):
        self.train_frac = train_frac
        self.val_frac = val_frac
        self.test_frac = test_frac
        self.batch_size = batch_size
        self.num_workers = num_workers

        self.dataset = []
        for it, t in enumerate(self.target_da.time.values):
            target = self.target_da.sel(time=t).values
            obs_vals = np.array([self.obs.ds[vn].sel(time=t).values for vn in self.obs.ds.data_vars])

            sample = {
                'obs_vals': torch.tensor(obs_vals, dtype=torch.float32),  # x
                'target': torch.tensor(target, dtype=torch.float32),      # y
            }
            self.dataset.append(sample)

        # Compute dataset indices
        ds_idx = list(range(len(self.dataset)))
        test_size = int(len(self.dataset) * self.test_frac)
        train_valid_size = len(self.dataset) - test_size
        
        # Split train+val and test sets
        self.train_valid_idx = ds_idx[:train_valid_size]
        self.test_idx = ds_idx[train_valid_size:]
        
        self.train_valid_set = torch.utils.data.Subset(self.dataset, self.train_valid_idx)
        self.test_set = torch.utils.data.Subset(self.dataset, self.test_idx)
        
        # Further split into train and validation sets
        train_size = int(self.train_frac / (self.train_frac + self.val_frac) * train_valid_size)
        val_size = train_valid_size - train_size
        self.train_set, self.valid_set = torch.utils.data.random_split(self.train_valid_set, [train_size, val_size])

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.train_set, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=True)

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.valid_set, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return torch.utils.data.DataLoader(self.test_set, batch_size=self.batch_size, num_workers=self.num_workers)



# class PseudoClimateDataset(torch.utils.data.Dataset):
#     def __init__(self, E=5, T=100, H=8, W=8, max_proxies=20):
#         self.E, self.T, self.H, self.W = E, T, H, W
#         self.prior = torch.randn(E, T, H, W)
#         self.true_field = self.prior.mean(dim=0) + 0.1 * torch.randn(T, H, W)

#         # Precompute proxy maps and masks with attrition
#         self.proxy_maps = []
#         self.proxy_masks = []

#         for t in range(T):
#             frac_available = (t + 1) / T  # More proxies in recent times
#             num_proxies = int(frac_available * max_proxies)

#             proxy_map = torch.zeros(H, W)
#             proxy_mask = torch.zeros(H, W)

#             for _ in range(num_proxies):
#                 h = torch.randint(0, H, (1,))
#                 w = torch.randint(0, W, (1,))
#                 val = self.true_field[t, h, w] + 0.2 * torch.randn(1)
#                 proxy_map[h, w] = val
#                 proxy_mask[h, w] = 1.0

#             self.proxy_maps.append(proxy_map)
#             self.proxy_masks.append(proxy_mask)

#     def __len__(self):
#         return self.T

#     def __getitem__(self, t):
#         x = (
#             self.prior[:, t],         # [E, H, W]
#             self.proxy_maps[t],       # [H, W]
#             self.proxy_masks[t],      # [H, W]
#         )
#         y = self.true_field[t]        # [H, W]
#         return x, y

# class Dataset(L.LightningDataModule):
#     def __init__(self, E=5, T=100, H=8, W=8, max_proxies=20,
#                  train_frac=0.7, val_frac=0.1, test_frac=0.2,
#                  batch_size=10, num_workers=4):
#         super().__init__()
#         self.batch_size = batch_size
#         self.num_workers = num_workers

#         self.dataset = PseudoClimateDataset(E=E, T=T, H=H, W=W, max_proxies=max_proxies)

#         assert abs(train_frac + val_frac + test_frac - 1.0) < 1e-6, 'Train, val, and test fractions must sum to 1.'
#         self.train_frac = train_frac
#         self.val_frac = val_frac
#         self.test_frac = test_frac

#     def setup(self, stage=None):
#         ds_idx = list(range(len(self.dataset)))
#         test_size = int(len(self.dataset) * self.test_frac)
#         train_valid_size = len(self.dataset) - test_size
        
#         # Split train+val and test sets
#         self.train_valid_idx = ds_idx[:train_valid_size]
#         self.test_idx = ds_idx[train_valid_size:]
#         train_valid_set = torch.utils.data.Subset(self.dataset, self.train_valid_idx)
#         self.test_set = torch.utils.data.Subset(self.dataset, self.test_idx)
        
#         # Further split into train and validation sets
#         train_size = int(self.train_frac / (self.train_frac + self.val_frac) * train_valid_size)
#         val_size = train_valid_size - train_size
#         self.train_set, self.valid_set = torch.utils.data.random_split(train_valid_set, [train_size, val_size])

#     def train_dataloader(self):
#         return torch.utils.data.DataLoader(self.train_set, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=True)

#     def val_dataloader(self):
#         return torch.utils.data.DataLoader(self.valid_set, batch_size=self.batch_size, num_workers=self.num_workers)

#     def test_dataloader(self):
#         return torch.utils.data.DataLoader(self.test_set, batch_size=self.batch_size, num_workers=self.num_workers)

#     def plot(self):
#         try:
#             import x4c
#         except ImportError:
#             raise ImportError('x4c is required for this method. Please install x4c via: pip install x4c-exp.')

#         x4c.set_style('journal_spines', font_scale=1.2)
#         fig, ax = plt.subplots(2, 2, figsize=(10, 9))

#         n_bins = 10
#         # Create discrete colormap from a continuous one
#         cmap = plt.get_cmap('RdBu_r', n_bins)  # 'n_bins' discrete colors from RdBu_r
#         bounds = np.linspace(-1, 1, n_bins + 1)  # edges of bins
#         norm = BoundaryNorm(bounds, n_bins)

#         ds = self.dataset
#         im = ax[0, 0].imshow(ds.true_field[-1], origin='lower', cmap=cmap, norm=norm)
#         ax[0, 0].set_xticks(range(0, ds.W, 1))
#         ax[0, 0].set_yticks(range(0, ds.H, 1))
#         ax[0, 0].set_xticklabels(range(0, ds.W, 1))
#         ax[0, 0].set_yticklabels(range(0, ds.H, 1))
#         ax[0, 0].grid(False)
#         ax[0, 0].set_title('True Field', weight='bold')
#         ax[0, 0].set_xlabel('Lon')
#         ax[0, 0].set_ylabel('Lat')

#         im = ax[0, 1].imshow(ds.prior[-1][0], origin='lower', cmap=cmap, norm=norm)
#         ax[0, 1].set_xticks(range(0, ds.W, 1))
#         ax[0, 1].set_yticks(range(0, ds.H, 1))
#         ax[0, 1].set_xticklabels(range(0, ds.W, 1))
#         ax[0, 1].set_yticklabels(range(0, ds.H, 1))
#         ax[0, 1].grid(False)
#         ax[0, 1].set_title('Prior Member: 0', weight='bold')
#         ax[0, 1].set_xlabel('Lon')
#         ax[0, 1].set_ylabel('Lat')

#         ax[1, 0].imshow(ds.proxy_maps[-1], origin='lower', cmap=cmap, norm=norm)
#         ax[1, 0].set_xticks(range(0, ds.W, 1))
#         ax[1, 0].set_yticks(range(0, ds.H, 1))
#         ax[1, 0].set_xticklabels(range(0, ds.W, 1))
#         ax[1, 0].set_yticklabels(range(0, ds.H, 1))
#         ax[1, 0].grid(False)
#         ax[1, 0].set_title('Proxy Map', weight='bold')
#         ax[1, 0].set_xlabel('Lon')
#         ax[1, 0].set_ylabel('Lat')

#         ax[1, 1].imshow(ds.proxy_masks[-1], origin='lower', cmap=cmap, norm=norm)
#         ax[1, 1].set_xticks(range(0, ds.W, 1))
#         ax[1, 1].set_yticks(range(0, ds.H, 1))
#         ax[1, 1].set_xticklabels(range(0, ds.W, 1))
#         ax[1, 1].set_yticklabels(range(0, ds.H, 1))
#         ax[1, 1].grid(False)
#         ax[1, 1].set_title('Proxy Mask', weight='bold')
#         ax[1, 1].set_xlabel('Lon')
#         ax[1, 1].set_ylabel('Lat')

#         cbar = fig.colorbar(im, ax=ax, shrink=0.7)
#         cbar.set_ticks(bounds)