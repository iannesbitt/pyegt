import time
import requests
from typing import Union, Literal

from . import defs

def get_ngs_json(lat: float, lon: float, ngs_model: int):
    """
    
    Variables:
    :param float lat: Decimal latitude
    :param float lon: Decimal longitude
    :param str ngs_model: The NGS geoid model to use for lookup `(see list) <https://www.ngs.noaa.gov/web_services/geoid.shtml>`_
    """
    ngs_url = defs.NGS_URL % (lat, lon, ngs_model)
    i = 0
    while True:
        print('Querying %s' % (ngs_url))
        response = requests.get(ngs_url)
        json_data = response.json() if response and response.status_code == 200 else None
        if json_data and 'geoidHeight' in json_data:
            print('Found geoidHeight value of %s' % (json_data['geoidHeight']))
            return json_data
        if json_data and (not 'geoidHeight' in json_data):
            print('Json data request returned in error: %s' % (json_data))
            exit(1)
        if i < 3:
            i += 1
            time.sleep(1)
        else:
            print('Could not complete request for NGS API in %s tries.' % (i  ))
            exit(1)

def get_vdatum_json(lat: float, lon: float, vdatum_model: str, region: str):
    """
    
    Variables:
    :param float lat: Decimal latitude
    :param float lon: Decimal longitude
    :param str vdatum_model: The VDatum geoid, tidal, or potential model to use for lookup `(see list) <https://vdatum.noaa.gov/docs/services.html#step160>`_
    """
    wgs = 'WGS84_G1674'
    r = 0
    if region == defs.REGIONS[0]:
        r = 1
    while True:
        vdatum_url = defs.VDATUM_URL % (
            lon, # s_x
            lat, # s_y
            wgs, # s_h_frame
            vdatum_model, # s_v_frame
            vdatum_model, # s_v_geoid
            wgs, # t_h_frame
            wgs, # t_v_frame
            vdatum_model, # t_v_geoid
            region # region
            )
        print('Querying %s' % (vdatum_url))
        response = requests.get(vdatum_url)
        json_data = response.json() if response and response.status_code == 200 else None
        if json_data and ('t_z' in json_data):
            return json_data
        if json_data and ('errorCode' in json_data):
            if 'Selected Region is Invalid!' in json_data['message']:
                # retry with different region
                region = defs.REGIONS[r]
                r += 1
                time.sleep(1)
                if r > len(defs.REGIONS):
                    raise AttributeError('No valid solution found! Tried with %s different VDatum regions' % (r+1))
                else:
                    continue
            else:
                raise AttributeError('VDatum API error %s: %s' % (json_data['errorCode'], json_data['message']))

"""def adjustment(user_vrs: Union[str, Literal[None]]=None,
               las_vrs: Union[str, Literal[None]]=None, # overrides user_vrs.
               # consequently implies we trust file headers;
               # this is done to support projects with multiple CRS
               # and to enforce correct CRS info in database
               lat:float=0.0, lon: float=0.0,
               region=defs.REGIONS[0]):
    ### docstring start
    Get the geoid, tidal, or geopotential model height above the ellipsoid
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
    to systems based on gravity or geopotential height. However, the earth and
    tides are influenced by local differences in gravitational pull and other
    factors. Therefore some engineering projects and local reference systems
    use height referenced to a geoid or tidal model (``H``) which provides a much
    easier framework to understand height relative to, for example, modeled
    mean sea level or sea level potential. Converting from ``H`` to ``h``
    requires knowing the height difference between the geoid and the ellipsoid
    (``N``).
    Conversion is then a simple addition of these values (``H + N = h``).

    This function will use either the
    `NGS <https://www.ngs.noaa.gov/web_services/geoid.shtml>`_ or
    `VDatum https://vdatum.noaa.gov/docs/services.html`_ API to look up
    geoid height relative to the ellipsoid (`N`).

    .. note::

        ``las_vrs`` is set by file headers and overrides ``user_vrs``.
        This implicitly means we trust file headers over user input.
        We do this to support projects with multiple VRS (i.e. `user_vrs`
        values are used solely to fill in gaps where headers do not explicitly
        specify a vertical reference system). It is also meant to enforce the
        accuracy of VRS information in file headers.

        If a project should need to set or change VRS information prior to
        uploading to the database, they are encouraged to do so through the
        use of third-party software such as
        `LASTools <https://github.com/LAStools/LAStools>`_.

    Variables:
    :param user_vrs: The user-specified geoid model to convert from if none is found in the file header
    :type user_vrs: str or None
    :param las_vrs: WKT-derived model from file header to convert from (overrides ``user_vrs``)
    :type las_vrs: str or None
    :param float lat: Decimal latitude
    :param float lon: Decimal longitude
    :param str region: The VDatum region `(see list in docs) <https://vdatum.noaa.gov/docs/services.html#step140>`_

    :return: 
    :rtype: int or pyproj.crs.CRS
    ### docstring end

    # the 9 possible scenarios and their outcomes
    # 1. matched las_vrs / matched user_vrs -> las_vrs
    # 2. matched las_vrs / unmatched user_vrs -> las_vrs
    # 3. matched las_vrs / empty user_vrs -> las_vrs
    # 4. empty las_vrs / empty user_vrs -> 0
    # 5. empty las_vrs / matched user_vrs -> user_vrs
    # 6. empty las_vrs / unmatched user_vrs -> exit(1)
    # 7. unmatched las_vrs / empty user_vrs -> exit(1)
    # 8. unmatched las_vrs / matched user_vrs -> exit(1) # maybe in the future we have a geoid_override setting where this will execute
    # 9. unmatched las_vrs / unmatched user_vrs -> exit(1)

    vrs = None
    if las_vrs:
        # override user value with detected VRS
        vrs = model_search(las_vrs)
        if user_vrs and vrs:
            # scenarios 1 and 2
            print('User value of "%s" will be overridden by detected VRS "%s"' % (user_vrs, vrs))
        if user_vrs and (not vrs):
            # scenarios 8 and 9
            print('No vertical reference system matching "%s" found' % (user_vrs))
            exit(1)
        if not user_vrs:
            # scenario 3
            pass
        if (not user_vrs) and (not vrs):
            # scenario 7
            print('No vertical reference system matching "%s" found' % (las_vrs))
    else:
        if not user_vrs:
            # scenario 4
            return 0
        else:
            vrs = model_search(user_vrs)
            if vrs:
                # scenario 5
                print('VRS found: %s (user-specified)' % (vrs))
            else:
                # scenario 6
                print('Could not find VRS matching value "%s"' % (user_vrs))
                exit(1)

    if vrs in defs.NGS_MODELS:
        # format url for NGS API, then interpret json response
        ngs_model = defs.NGS_MODELS[vrs]
        ngs_json = get_ngs_json(lat, lon, ngs_model)
        return float(ngs_json['geoidHeight'])
    if vrs in defs.VDATUM_MODELS:
        # format url for VDatum API, then interpret json response
        vdatum_json = get_vdatum_json(lat, lon, vrs, region)
        return float(vdatum_json['t_z'])
"""