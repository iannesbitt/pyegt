import json

from . import defs
from .height import HeightModel

def test():
    """
    Run tests. Tests will be run with the following parameters:

    - GEOID12B with US, AK, and PR coordinates::

        from pyegt.height import HeightModel
        HeightModel(lat=44.256616, lon=-73.964784, from_model='GEOID12B', region='contiguous')
        HeightModel(lat=64.486036, lon=-165.292154, from_model='GEOID12B', region='ak')
        HeightModel(lat=18.47131, lon=-66.136544, from_model='GEOID12B', region='prvi')

    - EGM2008 with US, AK, and PR coordinates::

        HeightModel(lat=44.256616, lon=-73.964784, from_model='EGM2008', region='contiguous')
        HeightModel(lat=64.486036, lon=-165.292154, from_model='EGM2008', region='ak')
        HeightModel(lat=18.47131, lon=-66.136544, from_model='EGM2008', region='prvi')

        
    Expected return height values::

        EXPECTED_VALUES = {
            'GEOID12B height': {
                'contiguous': -28.157,
                'ak': 5.28,
                'prvi': -43.285,
            },
            'EGM2008 height': {
                'contiguous': -28.899,
                'ak': 7.005,
                'prvi': -45.473,
            }
        }
    """
    TEST_COORDS = {
        defs.REGIONS[0]: {'lat': 44.256616, 'lon': -73.964784,}, # Jumping Complex, Lake Placid, NY
        defs.REGIONS[1]: {'lat': 64.486036, 'lon': -165.292154,}, # Nome River Bridge, Nome, AK
        defs.REGIONS[8]: {'lat': 18.471310, 'lon': -66.136544,}, # Isla de Cabras, Palo Seco, PR
    }
    MODELS = ['GEOID12B height',
              'EGM2008 height']
    EXPECTED_VALUES = {
        'GEOID12B height': {
            'contiguous': -28.157,
            'ak': 5.28,
            'prvi': -43.285,
        },
        'EGM2008 height': {
            'contiguous': -28.899,
            'ak': 7.005,
            'prvi': -45.473,
        }
    }
    TESTS = {}
    for m in MODELS:
        TESTS[m] = {}
        for t in TEST_COORDS:
            print('%s, %s' % (m, t))
            h = HeightModel(lat=TEST_COORDS[t]['lat'],
                            lon=TEST_COORDS[t]['lon'],
                            from_model=m, region=t)
            TESTS[m][t] = {'lookup': repr(h),
                            'height': float(h),
                            'expect': EXPECTED_VALUES[m][t],
                            'result': None}
            if TESTS[m][t]['lookup']:
                try:
                    assert TESTS[m][t]['height'] == TESTS[m][t]['expect']
                    TESTS[m][t]['result'] = True
                except AssertionError:
                    TESTS[m][t]['result'] = False
            else:
                TESTS[m][t]['result'] = False
    js = json.dumps(TESTS, indent=2)
    print(js)
    fail = False
    for m in TESTS:
        for t in m:
            if not TESTS[m][t]['result']:
                fail = True
                print('%s (%s) test has failed!' % (m, t))
    if fail:
        exit(1)
