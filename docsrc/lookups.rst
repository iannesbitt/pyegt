.. |geoid12b| raw:: html

   <a href="https://www.ngs.noaa.gov/GEOID/GEOID12B/" target="_blank">GEOID12B</a>

.. |ngsafg| raw:: html

   <a href="https://www.ngs.noaa.gov/web_services/geoid.shtml" target="_blank">NOAA NGS API for Geoid</a>

.. |vdatum| raw:: html

   <a href="https://vdatum.noaa.gov/docs/services.html" target="_blank">VDatum API</a>

Using pyegt
#####################################

``pyegt`` is designed to be easy to use.
Simply initialize a :py:class:`HeightModel` object to perform a datum lookup.
The following example uses the |ngsafg| to perform a lookup against
|geoid12b|.

.. code-block:: python

    >>> from pyegt.height import HeightModel
    >>> h = HeightModel(lat=44.256616, lon=-73.964784, from_model='GEOID12B')
    >>> repr(h)
    HeightModel(model='GEOID12B', lat=44.256616, lon=-73.964784, region='None') -> -28.157 meters
    >>> float(h)
    -28.157
    >>> h.in_feet_us_survey()
    -92.37842416572809

``pyegt`` can also be used to query the |vdatum| API. 

.. code-block:: python

    from pyegt.height import HeightModel
    h = HeightModel(lat=44.256616, lon=-73.964784, from_model='EGM2008', region='contiguous')

.. note:

    The ``region`` argument must be supplied for VDatum queries.
    If it is not supplied by the user, it will default to ``"contiguous"``.

.. note:

    VDatum and NGS geoid APIs are highly functional API software.
    ``pyegt`` is a wrapper that does not utilize all of their functionality.
    Its sole function is to perform lookups of ellipsoid height at
    specific locations on geoid and tidal models.
