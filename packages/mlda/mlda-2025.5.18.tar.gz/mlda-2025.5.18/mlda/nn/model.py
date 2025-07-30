import torch
import lightning as L
from .. import utils
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import x4c
import numpy as np

class CVAE(L.LightningModule):
    def __init__(self, prior_ens, obs_lats, obs_lons, obs_Rs, target_shape, lats,
                 latent_dim=32, hidden_dim=256, lr=1e-3):
        super().__init__()
        self.save_hyperparameters(ignore=["prior_ens", "obs_lats", "obs_lons", "obs_Rs", "lats"])
        self.weights = torch.cos(torch.deg2rad(torch.tensor(lats))).view(-1, 1)

        # Register buffers (conditions)
        self.register_buffer("prior_ens", prior_ens)
        self.register_buffer("obs_lats", obs_lats)
        self.register_buffer("obs_lons", obs_lons)
        self.register_buffer("obs_Rs", obs_Rs)

        self.n_proxies = obs_lats.shape[0]
        self.target_shape = target_shape  # (lat, lon)
        self.output_dim = target_shape[0] * target_shape[1]

        # Derived condition encoding
        self.condition_dim = self.n_proxies * 4 + prior_ens[0].numel()

        # Encoder
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(self.n_proxies + self.condition_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
        )
        self.fc_mu = torch.nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = torch.nn.Linear(hidden_dim, latent_dim)

        # Decoder
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(latent_dim + self.condition_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, self.output_dim)
        )

        self.lr = lr

    def encode(self, x, cond):
        inp = torch.cat([x, cond], dim=1)
        h = self.encoder(inp)
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z, cond):
        inp = torch.cat([z, cond], dim=1)
        return self.decoder(inp)

    def on_fit_start(self):
        self.weights = self.weights.to(self.device)

    def forward(self, obs_vals):
        # Handle NaNs in obs
        obs_mask = ~torch.isnan(obs_vals)
        obs_vals = torch.nan_to_num(obs_vals, nan=0.0)

        # Build condition: [batch, num_proxies * 4]
        bsz = obs_vals.shape[0]
        lat = self.obs_lats.unsqueeze(0).expand(bsz, -1)
        lon = self.obs_lons.unsqueeze(0).expand(bsz, -1)
        Rs = self.obs_Rs.unsqueeze(0).expand(bsz, -1)
        obs_cond = torch.cat([obs_vals, lat, lon, Rs], dim=1)  # [B, P*4]

        # Add prior ensemble mean (same for all samples)
        prior_feat = self.prior_ens.flatten(start_dim=1).mean(0).expand(bsz, -1)  # [B, prior_dim]
        cond = torch.cat([obs_cond, prior_feat], dim=1)  # [B, condition_dim]

        # CVAE steps
        mu, logvar = self.encode(obs_vals, cond)
        z = self.reparameterize(mu, logvar)
        recon = self.decode(z, cond)
        recon = recon.view(-1, *self.target_shape)  # Reshape to [B, lat, lon]
        return recon, mu, logvar

    def training_step(self, batch, batch_idx):
        obs_vals = batch['obs_vals']
        target = batch['target']

        recon, mu, logvar = self.forward(obs_vals)
        target = target.view_as(recon)

        loss_recon = torch.nn.functional.mse_loss(recon, target, reduction='mean')
        loss_recon = (loss_recon * self.weights).mean()
        loss_kl = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
        loss = loss_recon + loss_kl

        self.log_dict(
            {'train_loss': loss, 'recon_loss': loss_recon, 'kl_loss': loss_kl},
            on_step=True, on_epoch=True, prog_bar=True, sync_dist=True,
        )
        return loss

    def validation_step(self, batch, batch_idx):
        obs_vals = batch['obs_vals']
        target = batch['target']
        recon, mu, logvar = self.forward(obs_vals)
        target = target.view_as(recon)

        loss_recon = torch.nn.functional.mse_loss(recon, target, reduction='mean')
        loss_recon = (loss_recon * self.weights).mean()
        loss_kl = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
        loss = loss_recon + loss_kl

        self.log_dict(
            {'valid_loss': loss, 'recon_loss': loss_recon, 'kl_loss': loss_kl},
            on_step=True, on_epoch=True, prog_bar=True, sync_dist=True,
        )

        # loss = loss_recon
        # self.log_dict(
        #     {'valid_loss': loss},
        #     on_step=True, on_epoch=True, prog_bar=True, sync_dist=True,
        # )

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)