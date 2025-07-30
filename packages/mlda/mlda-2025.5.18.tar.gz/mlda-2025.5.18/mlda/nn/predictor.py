import os
import xarray as xr
import numpy as np
import torch
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
)

from .. import utils

class Predictor:
    def __init__(self, model, data, ckpt_fpath):
        self.model = model
        self.data = data
        self.ckpt_fpath = ckpt_fpath
        self.ckpt = torch.load(self.ckpt_fpath, weights_only=True)
        self.model.load_state_dict(self.ckpt['state_dict'])

    def run(self, pred_fpath=None, truth_fpath=None, set='test'):
        if set == 'train':
            dataset = self.data.train_valid_set
            idx_start = self.data.train_valid_idx[0]
            idx_end = self.data.train_valid_idx[-1]
        elif set == 'test':
            dataset = self.data.test_set
            idx_start = self.data.test_idx[0]
            idx_end = self.data.test_idx[-1]

        self.y = [data['target'].detach().numpy() for data in dataset]
        self.y_hat = [self.model.forward(data['obs_vals'].unsqueeze(0))[0].squeeze(0).detach().numpy() for data in dataset]

        self.da_truth = xr.DataArray()
        self.da_pred = xr.Dataset()

        ds_template = self.data.target_da[idx_start:idx_end+1]
        self.da_truth = ds_template.copy()
        self.da_truth.values = np.array(self.y)
        self.da_pred = ds_template.copy()
        self.da_pred.values = np.array(self.y_hat)

        if truth_fpath is not None:
            if os.path.exists(truth_fpath): os.remove(truth_fpath)
            dirpath = os.path.dirname(truth_fpath)
            if not os.path.exists(dirpath): os.makedirs(dirpath, exist_ok=True)
            self.ds_truth.to_netcdf(truth_fpath)
            utils.p_success(f'Truth saved at: "{truth_fpath}"')

        if pred_fpath is not None:
            if os.path.exists(pred_fpath): os.remove(pred_fpath)
            dirpath = os.path.dirname(pred_fpath)
            if not os.path.exists(dirpath): os.makedirs(dirpath, exist_ok=True)
            self.ds_pred.to_netcdf(pred_fpath)
            utils.p_success(f'Prediction saved at: "{pred_fpath}"')

    def plot(self, t_idx=None, figsize=(16, 10), nrow=3, ncol=2, ax_loc=None, projs=None, projs_kws=None, wspace=0.1, hspace=0.2, **kws):
        try:
            import x4c
        except ImportError:
            raise ImportError('x4c is required for this method. Please install x4c via: pip install x4c-exp.')

        x4c.set_style('journal_spines', font_scale=1.2)
        ax_loc={
            'Truth': (0, 0),
            'Pred': (1, 0),
            'Diff': (2, 0),
            'corr': (0, 1),
            'R2': (1, 1),
            'RMSE': (2, 1),
        } if ax_loc is None else ax_loc

        projs={
            'Truth': 'Robinson',
            'Pred': 'Robinson',
            'Diff': 'Robinson',
            'corr': 'Robinson',
            'R2': 'Robinson',
            'RMSE': 'Robinson',
        } if projs is None else projs

        projs_kws={
            'Truth': {'central_longitude': 180},
            'Pred': {'central_longitude': 180},
            'Diff': {'central_longitude': 180},
            'corr': {'central_longitude': 180},
            'R2': {'central_longitude': 180},
            'RMSE': {'central_longitude': 180},
        } if projs_kws is None else projs_kws

        if t_idx is None:
            if len(self.da_truth.dims) > 1 and 'time' in self.da_truth.dims:
                da_truth = self.da_truth.mean('time')
        else:
            ax_loc.pop('corr')
            ax_loc.pop('R2')
            ax_loc.pop('RMSE')
            projs.pop('corr')
            projs.pop('R2')
            projs.pop('RMSE')
            projs_kws.pop('corr')
            projs_kws.pop('R2')
            projs_kws.pop('RMSE')
            figsize = (16, 10)
            ncol = 1
            da_truth = self.da_truth.isel(time=t_idx)

        if t_idx is None:
            if len(self.da_pred.dims) > 1 and 'time' in self.da_pred.dims:
                da_pred = self.da_pred.mean('time')
        else:
            da_pred = self.da_pred.isel(time=t_idx)

        fig, ax = x4c.visual.subplots(
            nrow=nrow, ncol=ncol,
            ax_loc=ax_loc,
            projs=projs,
            projs_kws=projs_kws,
            figsize=figsize,
            wspace=wspace,
            hspace=hspace,
        )

        _kws_truth = kws.copy()
        _kws_truth.update({
            'title': 'Truth',
        })
        da_truth.x.plot(ax=ax['Truth'], **_kws_truth)

        _kws_pred = kws.copy()
        _kws_pred.update({
            'title': 'Prediction',
        })
        da_pred.x.plot(ax=ax['Pred'], **_kws_pred)

        _kws_diff = kws.copy()
        _kws_diff.update({
            'levels': np.linspace(-1, 1, 11),
            'cbar_kwargs': {
                'ticks': np.linspace(-1, 1, 11),
            },
            'title': 'Prediction $-$ Truth',
        })
        diff = da_pred - da_truth
        diff.x.plot(ax=ax['Diff'], **_kws_diff)

        if t_idx is None:
            _kws_corr = kws.copy()
            _kws_corr.update({
                'levels': np.linspace(-1, 1, 11),
                'cbar_kwargs': {
                    'ticks': np.linspace(-1, 1, 11),
                    'label': r'$r$',
                },
                'title': 'Corr(Prediction, Truth)',
            })
            corr = xr.corr(self.da_pred, self.da_truth, dim='time')
            corr.x.plot(ax=ax['corr'], **_kws_corr)

            _kws_R2 = kws.copy()
            _kws_R2.update({
                'levels': np.linspace(0, 1, 11),
                'cbar_kwargs': {
                    'ticks': np.linspace(0, 1, 11),
                    'label': r'R$^2$',
                },
                'extend': 'min',
                'title': r'R$^2$(Prediction, Truth)',
            })
            R2 = xr.apply_ufunc(
                r2_score,
                self.da_pred,
                self.da_truth,
                input_core_dims=[['time'], ['time']],  # Apply along the 'time' dimension
                vectorize=True,
            )
            R2.x.plot(ax=ax['R2'], **_kws_R2)

            _kws_RMSE = kws.copy()
            _kws_RMSE.update({
                'levels': np.linspace(-1, 1, 11),
                'cbar_kwargs': {
                    'ticks': np.linspace(-1, 1, 11),
                    'label': 'RMSE',
                },
                'extend': 'both',
                'title': 'RMSE(Prediction, Truth)',
            })
            MSE = xr.apply_ufunc(
                mean_squared_error,
                self.da_pred,
                self.da_truth,
                input_core_dims=[['time'], ['time']],  # Apply along the 'time' dimension
                vectorize=True,
            )
            RMSE = np.sqrt(MSE)
            RMSE.x.plot(ax=ax['RMSE'], **_kws_RMSE)

        return fig, ax