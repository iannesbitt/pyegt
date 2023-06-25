# pyegt

**Ellipsoid-relative geoid and tidal model height lookup**

*Ian Nesbitt, NCEAS-UCSB*

[![PyPI](https://img.shields.io/pypi/v/pyegt)](https://pypi.org/project/pyegt)
[![Conda](https://img.shields.io/conda/v/iannesbitt/pyegt)](https://anaconda.org/iannesbitt/readgssi)

`pyegt` is an open source program developed by [NCEAS](https://nceas.ucsb.edu)
to look up the geoid, tidal, or geopotential model height above the ellipsoid
in order to convert model-referenced heights to ellipsoid height (i.e.
compatible with [Cesium](https://cesium.com)) and vice-versa.

## About

The following figure demonstrates the difference between geoid, ellipsoid,
and topographic ground surface:

![Ellipsoid, geoid, and topography](https://user-images.githubusercontent.com/18689918/239385604-5b5dd0df-e2fb-4ea9-90e7-575287a069e6.png)

The figure shows a diagram with a conceptual model of ellipsoid height `h`, geoid
height `H`, and height of geoid relative to ellipsoid `N`
along with topographic surface (grey).

Ellipsoidal height (`h`) is generally used in global projections such as
Cesium due to its small digital footprint and ease of calculation relative
to systems based on gravity or geopotential height. However, gravity and
tides are influenced by local differences in Earth's density and other
factors. Therefore some projects prefer reference systems that use height
referenced to a geoid or tidal model (`H`) which provides a much easier
framework to understand height relative to, for example, modeled mean sea
level or sea level potential. Converting from `H` to `h` requires
knowing the height difference between the geoid and the ellipsoid (`N`).
Conversion is then a simple addition of these values (`H + N = h`).

## Usage

```python
>>> from pyegt.height import HeightModel
>>> h = HeightModel(lat=44.256616, lon=-73.964784, from_model='GEOID12B')
>>> repr(h)
HeightModel(lat=44.256616, lon=-73.964784, from_model='GEOID12B', region='None') -> -28.157 meters
>>> float(h)
-28.157
>>> h.in_feet_us_survey()
-92.37842416572809
```
