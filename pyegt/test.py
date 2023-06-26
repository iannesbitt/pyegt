import json

from . import defs
from .height import HeightModel

def test():
    """
    Run tests.

    - Try GEOID12B with US, AK, and PR coordinates.

    - Try EGM2008 with US, AK, and PR coordinates.
    """
    TEST_COORDS = {
        defs.REGIONS[0]: {'lat': 44.256616, 'lon': -73.964784,}, # Jumping Complex, Lake Placid, NY
        defs.REGIONS[1]: {'lat': 64.486036, 'lon': -165.292154,}, # Nome River Bridge, Nome, AK
        defs.REGIONS[8]: {'lat': 18.471310, 'lon': -66.136544,}, # Isla de Cabras, Palo Seco, PR
    }
    MODELS = ['GEOID12B height',
              'EGM2008 height']
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
                            'result': None}
            if TESTS[m][t]['lookup']:
                repr(TESTS[m][t]['lookup'])
                TESTS[m][t]['result'] = True
            else:
                TESTS[m][t]['result'] = False
    js = json.dumps(TESTS, indent=2)
    print(js)
