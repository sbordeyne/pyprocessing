from pyprocessing import PyProcessing


def stroke_cap(cap):
    pp = PyProcessing()
    if cap == 1:
        pp.namespace['stroke_cap_attribute'] = 'butt'
    elif cap == 2:
        pp.namespace['stroke_cap_attribute'] = 'round'
    elif cap == 4:
        pp.namespace['stroke_cap_attribute'] = 'projecting'
    else:
        pp.namespace['stroke_cap_attribute'] = 'butt'


def stroke_weight(weight):
    pp = PyProcessing()
    pp.namespace['stroke_thickness_attribute'] = weight


def stroke_join(join):
    pp = PyProcessing()
    if join == 2:
        pp.namespace['stroke_join_attribute'] = 'round'
    elif join == 8:
        pp.namespace['stroke_join_attribute'] = 'miter'
    elif join == 32:
        pp.namespace['stroke_join_attribute'] = 'bevel'
    else:
        pp.namespace['stroke_join_attribute'] = 'bevel'
