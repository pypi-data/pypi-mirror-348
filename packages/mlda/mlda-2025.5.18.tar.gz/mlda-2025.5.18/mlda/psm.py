import xarray as xr
import pybaywatch as pb
import numpy as np

from . import utils
from . import obs

class IdenticalTS:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['TS', 'tas']

    def forward(self):
        if 'TEMP' in self.record.clim:
            self.output = self.record.clim['TS'].values
        elif 'tas' in self.record.clim:
            self.output = self.record.clim['tas'].values

class IdenticalSST:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['TEMP', 'sst']

    def forward(self):
        if 'TEMP' in self.record.clim:
            self.output = self.record.clim['TEMP'].isel(z_t=0).values
        elif 'sst' in self.record.clim:
            self.output = self.record.clim['sst'].values

class IdenticalSSS:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['SALT']

    def forward(self):
        self.output = self.record.clim['SALT'].isel(z_t=0).values

class IdenticalSSTSSS:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['TEMP', 'SALT']

    def forward(self):
        self.output = self.record.clim['TEMP'].isel(z_t=0).values+self.record.clim['SALT'].isel(z_t=0).values

class TEX86:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['TEMP', 'tos', 'sst']

    def forward(self, seed=2333, mode='analog', type='SST', tolerance=1):
        if 'TEMP' in self.record.clim:
            sst = self.record.clim['TEMP'].isel(z_t=0).values
        elif 'tos' in self.record.clim:
            sst = self.record.clim['tos'].values
        elif 'sst' in self.record.clim:
            sst = self.record.clim['sst'].values

        lat = self.record.data.lat
        lon = self.record.data.lon
        lon180 = utils.lon180(lon)

        # run
        self.params = {
            'lat': lat,
            'lon': lon180,
            'temp': sst,
            'seed': seed,
            'type': type,
            'mode': mode,
            'tolerance': tolerance,
        }
        res = pb.TEX_forward(**self.params)
        if res['status'] == 'FAIL':
            utils.p_warning(f'>>> Forward modeling failed for proxy: {self.meta["pid"]}')
            self.output = None
        else:
            self.output = np.median(res['values'], axis=1)

class UK37:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['TEMP', 'tos', 'sst']

    def forward(self, order=3, seed=2333):
        if 'TEMP' in self.record.clim:
            sst = self.clim['TEMP'].isel(z_t=0).values
        elif 'tos' in self.record.clim:
            sst = self.record.clim['tos'].values
        elif 'sst' in self.record.clim:
            sst = self.record.clim['sst'].values

        # run
        self.params = {
            'sst': sst,
            'order': order,
            'seed': seed,
        }
        res = pb.UK_forward(**self.params)
        self.output = np.median(res['values'], axis=1)

class MgCa:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['TEMP', 'tos', 'sst', 'SALT', 'sos', 'sss']

    def forward(self, age, omega=None, pH=None, clean=None, species=None, sw=2, H=1, seed=2333):
        if 'TEMP' in self.record.clim and 'SALT' in self.record.clim:
            sst = self.record.clim['TEMP'].isel(z_t=0).values
            sss = self.record.clim['SALT'].isel(z_t=0).values
        elif 'tos' in self.record.clim and 'sos' in self.record.clim:
            sst = self.record.clim['tos'].values
            sss = self.record.clim['sos'].values
        elif 'sst' in self.record.clim and 'sss' in self.record.clim:
            sst = self.record.clim['sst'].values
            sss = self.record.clim['sss'].values

        # get omega and pH
        lat = self.record.data.lat
        lon = self.record.data.lon
        depth = self.record.data.depth
        if omega is None and pH is None:
            lon180 = np.mod(lon + 180, 360) - 180
            omega, pH = pb.core.omgph(lat, lon180, depth)

        if clean is None: clean = self.record.data.clean
        if species is None: species = self.record.data.species

        # run
        self.params = {
            'age': age,
            'sst': sst,
            'salinity': sss,
            'pH': pH,
            'omega': omega,
            'species': species,
            'clean': clean,
            'sw': sw,
            'H': H,
            'seed': seed,
        }
        res = pb.MgCa_forward(**self.params)
        self.output = np.median(res['values'], axis=1)

class d18Oc:
    def __init__(self, record:obs.ProxyRecord=None):
        self.record = record

    @property
    def clim_vns(self):
        return ['TEMP', 'tos', 'sst', 'SALT', 'sos', 'sss', 'd18Osw']

    def forward(self, pH=None, species=None, pH_type=0, seed=2333):
        if 'TEMP' in self.record.clim and 'SALT' in self.record.clim:
            sst = self.record.clim['TEMP'].isel(z_t=0).values
            sss = self.record.clim['SALT'].isel(z_t=0).values
        elif 'tos' in self.record.clim and 'sos' in self.record.clim:
            sst = self.record.clim['tos'].values
            sss = self.record.clim['sos'].values
        elif 'sst' in self.record.clim and 'sss' in self.record.clim:
            sst = self.record.clim['sst'].values
            sss = self.record.clim['sss'].values

        d18Osw = self.record.clim['d18Osw'].values
        if pH is None: pH = self.record.data.species
        if species is None: species = self.record.data.species

        # run
        self.params = {
            'sst': sst,
            'd18Osw': d18Osw,
            'sss': sss,
            'pH': pH,
            'pH_type': pH_type,
            'species': species,
            'seed': seed,
        }
        res = pb.d18Oc_forward(**self.params)
        self.output = np.median(res['values'], axis=1)