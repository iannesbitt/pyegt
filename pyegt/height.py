from pathlib import Path
from typing import Union, Literal
from pyproj import CRS
from math import isclose

from . import defs
from . import utils

class HeightModel:
    """
    Look up the geoid, tidal, or geopotential model height above the ellipsoid
    in order to convert model-referenced heights to ellipsoid height (i.e.
    compatible with Cesium) and vice-versa.

    The following figure demonstrates the difference between geoid, ellipsoid,
    and topographic ground surface:

    .. figure:: https://user-images.githubusercontent.com/18689918/239385604-5b5dd0df-e2fb-4ea9-90e7-575287a069e6.png
        :align: center

        Diagram showing conceptual model of ellipsoid height ``h``, geoid
        height ``H``, and height of geoid relative to ellipsoid ``N``
        along with topographic surface (grey).

    Ellipsoidal height (``h``) is generally used in global projections such as
    Cesium due to its small digital footprint and ease of calculation relative
    to systems based on gravity or geopotential height. However, gravity and
    tides are influenced by local differences in Earth's density and other
    factors. Therefore some projects prefer reference systems that use height
    referenced to a geoid or tidal model (``H``) which provides a much easier
    framework to understand height relative to, for example, modeled mean sea
    level or sea level potential. Converting from ``H`` to ``h`` requires
    knowing the height difference between the geoid and the ellipsoid (``N``).
    Conversion is then a simple addition of these values (``H + N = h``).

    The lookup performed by this :class:`pyegt.height.HeightModel` class will
    use either the `NGS <https://www.ngs.noaa.gov/web_services/geoid.shtml>`_
    or `VDatum <https://vdatum.noaa.gov/docs/services.html>`_ API to look up
    model height relative to the ellipsoid (``N``).


    :param float lat: Decimal latitude
    :param float lon: Decimal longitude
    :param region: Region (for list see :py:func:`pyegt.height.HeightModel.from_model`)
    :type region: str or None
    :param from_model: Model (for list see :py:func:`pyegt.height.HeightModel.available_regions`)
    :type from_model: str or None
    :param from_vrs: The vertical reference system to convert from (``CRS.is_vertical`` must be true for the main CRS or a sub-CRS)
    :type from_vrs: pyproj.CRS or None
    :param from_wkt: Use well-known text to get a VRS to convert from
    :type from_wkt: str or None
    :param from_epsg: Use an EPSG code to get a VRS to convert from
    :type from_epsg: str or None
    """
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
        self.url = None
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
        Compute the height above the ellipsoid for the given model.
        Will set ``self.model`` if the ``model`` variable is supplied.
        Finally, it will call ``self.get_height()``.

        Valid model values are::

            # using NGS API
            ['GEOID99', 'G99SSS', 'GEOID03', 'USGG2003', 'GEOID06', 'USGG2009',
            'GEOID09', 'XUSHG', 'USGG2012', 'GEOID12A', 'GEOID12B', 'GEOID18',]

            # using VDatum API
            ['NAVD88', 'NGVD29', 'ASVD02', 'W0_USGG2012', 'GUVD04', 'NMVD03',
            'PRVD02', 'VIVD09', 'CRD', 'EGM2008', 'EGM1996', 'EGM1984',
            'XGEOID16B', 'XGEOID17B', 'XGEOID18B', 'XGEOID19B', 'XGEOID20B',
            'IGLD85', 'LWD_IGLD85', 'OHWM_IGLD85', 'CRD', 'LMSL', 'MLLW',
            'MLW', 'MTL', 'DTL', 'MHW', 'MHHW', 'LWD', 'NAD27', 'NAD83_1986',
            'NAD83_2011', 'NAD83_NSRS2007', 'NAD83_MARP00', 'NAD83_PACP00',
            'WGS84_G1674', 'ITRF2014', 'IGS14', 'ITRF2008', 'IGS08',
            'ITRF2005', 'IGS2005', 'WGS84_G1150', 'ITRF2000', 'IGS00', 'IGb00',
            'ITRF96', 'WGS84_G873', 'ITRF94', 'ITRF93', 'ITRF92', 'SIOMIT92',
            'WGS84_G730', 'ITRF91', 'ITRF90', 'ITRF89', 'ITRF88',
            'WGS84_TRANSIT', 'WGS84_G1762', 'WGS84_G2139']

        Documentation can be found here for the
        `NGS <https://www.ngs.noaa.gov/web_services/geoid.shtml>`_ and
        `VDatum <https://vdatum.noaa.gov/docs/services.html>`_ APIs.
        """
        if (not model) and (not self.model):
            raise AttributeError('Cannot calculate model height, as no model has been set.')
        if model:
            self.model = model
        self.model = self.model.upper()
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
        return self.from_model(self.vrs.name)

    def from_wkt(self, wkt: Union[str, Literal[None]]):
        """
        """
        rs = CRS.from_wkt(wkt)
        return self.from_vrs(rs)

    def from_epsg(self, epsg: Union[str, int, Literal[None]]):
        """
        """
        rs = CRS.from_epsg(epsg)
        return self.from_vrs(rs)

    def verify_model(self) -> bool:
        """
        Search for a model in the list of known models.
        
        :param str vrs: The search term, potentially a phrase containing the model name; ex: ``EGM2008 height`` will return ``EGM2008``
        :return: Returns the correctly formatted model name to use in the API query
        :rtype: str
        """
        for m in defs.MODEL_LIST:
            if m in self.model.upper():
                # sometimes las_vrs will be formatted like "EGM2008 height" and this should catch that
                self.model = m
                return True
        return False

    def get_height(self) -> float:
        """
        """
        if not self.verify_model():
            raise ValueError('No model found matching "%s"' % (self.model))
        if self.model in defs.NGS_MODELS:
            # format url for NGS API, then interpret json response
            ngs_model = defs.NGS_MODELS[self.model]
            self.url = utils.get_ngs_url(self.lat, self.lon, ngs_model)
            self.json = utils.get_ngs_json(self.url)
            self.height = float(self.json['geoidHeight'])
            return float(self.json['geoidHeight'])
        if self.model in defs.VDATUM_MODELS:
            # format url for VDatum API, then interpret json response
            if not self.region:
                self.region = defs.REGIONS[0]
                print('Warning: no region set. Defaulting to "%s"' % (self.region))
            else:
                self.region = self.region.lower()
            self.url = utils.get_vdatum_url(lat=self.lat, lon=self.lon, vdatum_model=self.model, region=self.region)
            self.json = utils.get_vdatum_json(self.url, self.region)
            self.height = float(self.json['t_z'])
            return float(self.json['t_z'])

    def in_feet_us_survey(self) -> float:
        """
        Convert to US survey foot (for imperial feet use `in_feet()`).
        1 imperial foot = 0.999998 US survey feet

        :return: Height value in usft (if it exists)
        :rtype: float
        """
        if self.height:
            return self.height * 3.2808333333

    def in_feet(self) -> float:
        """
        Convert to imperial foot (for US survey feet use `in_feet_us_survey()`).
        1 imperial foot = 0.999998 US survey feet

        :return: Height value in ft (if it exists)
        :rtype: float
        """
        if self.height:
            return self.height * 3.280839895
    
    def in_cm(self) -> float:
        """
        Convert to centimeters.

        :return: Height value in cm (if it exists)
        :rtype: float
        """
        if self.height:
            return self.height * 100

    def __str__(self) -> str:
        """
        Convert to string.

        :return: String representation of height or ``"n/a"``
        :rtype: str
        """
        if self.height:
            return '%s' % (self.height)
        else:
            return 'n/a'

    def as_string(self) -> str:
        """
        Convert to string using ``__str__``.

        :return:
        :rtype: str
        """
        return self.__str__()

    def available_models(self) -> list:
        """
        Return a list of available geoid and tidal models.

        :return: List of models
        :rtype: list
        """
        return defs.MODEL_LIST

    def available_regions(self) -> list:
        """
        Return a list of regions usable with VDatum models.
        See `VDatum regions <https://vdatum.noaa.gov/docs/services.html#step140>`_
        in the docs.

        Regions::

            ['contiguous', 'ak', 'seak', 'as', 'chesapeak_delaware',
            'westcoast', 'gcnmi', 'hi', 'prvi', 'sgi', 'spi', 'sli']

        :return: List of regions
        :rtype: list
        """
        return defs.REGIONS

    def __repr__(self) -> str:
        """
        Convert to printable representation, for example::

            >>> from pyegt.height import HeightModel
            >>> h = HeightModel(lat=64.506181, lon=-165.399282, from_model='EGM2008', region='ak')
            >>> repr(h)
            HeightModel(lat=64.506181, lon=-165.399282, from_model='EGM2008', region='ak') -> 6.998 meters

        :return: repr() value
        :rtype: str
        """
        if self.height:
            return "HeightModel(lat=%s, lon=%s, from_model='%s', region='%s') -> %s meters" % (self.lat, self.lon, self.model, self.region, self.height)
        else:
            return "HeightModel()"

    def __float__(self) -> float:
        """
        Convert to float.

        :return: Height value (if exists)
        :rtype: float
        """
        if self.height:
            return self.height
        else:
            raise ValueError('Cannot convert to float when no height has been calculated.')

    def as_float(self) -> float:
        """
        Convert to float using ``__float__``.

        :return: Height value (if exists)
        :rtype: float
        """
        return self.float()
    
    def __dict__(self) -> dict:
        """
        Return JSON object as dict.

        :return: JSON object
        :rtype: dict
        """
        if self.json:
            return self.json
        else:
            return None
        
    def as_dict(self) -> dict:
        """
        Return JSON object as dict using ``__dict__``.

        :return: JSON object
        :rtype: dict
        """
        return self.__dict__()

    def __eq__(self, __value: object) -> bool:
        """
        Use `math.isclose()` to compare as floating point numbers are not always directly comparable.

        :return: Boolean equality of two floats
        :rtype: bool
        """
        if self.height:
            return isclose(self.height, float(__value), rel_tol=1e-9, abs_tol=0.0)
        else:
            raise ValueError('Cannot compare when no height has been calculated.')
