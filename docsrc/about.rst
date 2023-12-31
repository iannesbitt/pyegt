.. |nceas| raw:: html

    <a href="https://nceas.ucsb.edu" target="_blank">NCEAS</a>

.. |cesium| raw:: html

    <a href="https://cesium.com" target="_blank">Cesium</a>

About pyegt
#####################################

``pyegt`` is an open source program developed by |nceas| to look up
the geoid, tidal, or geopotential model height above the ellipsoid
in order to convert model-referenced heights to ellipsoid height (i.e.
compatible with |cesium|) and vice-versa.

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

The lookup performed by the :class:`pyegt.height.HeightModel` class will
use either the `NGS <https://www.ngs.noaa.gov/web_services/geoid.shtml>`_
or `VDatum <https://vdatum.noaa.gov/docs/services.html>`_ API to look up
model height relative to the ellipsoid (``N``).

.. note::

    ``pyegt`` is a wrapper around the NGS and VDatum APIs, but not all
    functionality of those APIs has been included in this software.
    Please read the documentation and consider contributing to the codebase
    if you feel strongly about missing features.
