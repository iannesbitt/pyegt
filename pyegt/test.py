from . import defs
from .height import HeightModel

def test():
    """
    Run tests.

    Try GEOID12B with US, AK, and PR coordinates.

    Try EGM2008 with US, AK, and PR coordinates.
    """
    TEST_COORDS = {
        defs.REGIONS[0]: {'lat': 0, 'lon': 0,},
        defs.REGIONS[1]: {'lat': 0, 'lon': 0,},
        defs.REGIONS[2]: {'lat': 0, 'lon': 0,},
    }
    MODELS = ['GEOID12B height',
              'EGM2008 height']
    TESTS = {}
    for m in MODELS:
        for t in TEST_COORDS:
            m = '%s, %s' % (m, t)
            TESTS[m] = {'lookup': HeightModel(lat=TEST_COORDS[t]['lat'],
                                              lon=TEST_COORDS[t]['lon'],
                                              from_model=m,),
                        'result': None}
            if TESTS[m]['lookup']:
                TESTS[m]['result'] = True
            else:
                TESTS[m]['result'] = False