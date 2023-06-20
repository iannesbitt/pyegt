from pathlib import Path
from typing import Union, Literal
from pyproj import CRS

from . import defs
from . import utils

class HeightModel:
    def __init__(self,
                 lat: float,
                 lon: float,
                 region: Union[str, Literal[None]]=None,
                 from_model: Union[str, Literal[None]]=None,
                 from_vrs: Union[CRS, Literal[None]]=None,
                 from_wkt: Union[str, Literal[None]]=None,
                 from_epsg: Union[str, int, Literal[None]]=None,
                 ) -> None:
        self.lat = lat
        self.lon = lon
        self.vrs = from_vrs
        self.model = from_model
        self.region = region
        self.wkt = from_wkt
        self.epsg = from_epsg
        self.height = None
        if from_model and (not from_wkt and not from_epsg and not from_vrs):
            self.from_model()
        elif from_vrs and (not from_wkt and not from_epsg and not from_model):
            self.from_vrs()
        elif from_wkt and (not from_vrs and not from_epsg and not from_model):
            self.from_wkt()
        elif from_epsg and (not from_vrs and not from_wkt and not from_model):
            self.from_epsg()
        elif (not from_vrs and not from_epsg and not from_wkt and not from_model):
            # starting out with a blank slate
            self.vrs = None
        else:
            raise AttributeError('Only one of the parameters [from_model, from_vrs, from_wkt, from_epsg] can be set at once to avoid collisions.')
    
    def from_model(self, model: Union[str, Literal[None]]=None):
        """
        """
        if (not model) and (not self.model):
            raise AttributeError('Cannot calculate model height, as no model has been set.')
        if model:
            self.model = model
        return self.get_height()
        
    def from_vrs(self, vrs: Union[CRS, Literal[None]]):
        """
        """
        if (not vrs) and (not self.vrs):
            raise AttributeError('Cannot calculate VRS height, as no VRS has been set.')
        if vrs:
            self.vrs = vrs
        if self.vrs.is_compound:
            for rs in self.vrs.sub_crs_list:
                if rs.is_vertical:
                    self.vrs = rs
        elif self.vrs.is_vertical:
            self.vrs = vrs
        self.from_model(self.vrs.name)
    def from_wkt(self, wkt: Union[str, Literal[None]]):
        """
        """
        rs = CRS.from_wkt(wkt)
        self.from_vrs(rs)
    def from_epsg(self, epsg: Union[str, int, Literal[None]]):
        """
        """
        rs = CRS.from_epsg(epsg)
        self.from_vrs(rs)

    def verify_model(self):
        """

        Variables:
        :param str vrs: 
        """
        for m in defs.MODEL_LIST:
            if m in self.model:
                # sometimes las_vrs will be formatted like "EGM2008 height" and this should catch that
                self.model = m
                return True
        return False

    def get_height(self):
        """
        """
        if not self.verify_model():
            raise ValueError('No model found matching "%s"' % (self.model))
        if self.model in defs.NGS_MODELS:
            # format url for NGS API, then interpret json response
            ngs_model = defs.NGS_MODELS[self.model]
            ngs_json = utils.get_ngs_json(self.lat, self.lon, ngs_model)
            self.height = float(ngs_json['geoidHeight'])
            return float(ngs_json['geoidHeight'])
        if self.model in defs.VDATUM_MODELS:
            # format url for VDatum API, then interpret json response
            if self.region:
                vdatum_json = utils.get_vdatum_json(lat=self.lat, lon=self.lon, vdatum_model=self.vrs, region=self.region)
                self.height = float(vdatum_json['t_z'])
                return float(vdatum_json['t_z'])
            else:
                vdatum_json = utils.get_vdatum_json(lat=self.lat, lon=self.lon, vdatum_model=self.vrs, region=defs.REGIONS[0])
                return float(vdatum_json['t_z'])
