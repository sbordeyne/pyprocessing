from pyprocessing import PyProcessing


def stroke_cap(cap):
    pp = PyProcessing()
    if cap == 1:
        pp.namespace['stroke_cap'] = 'butt'
    elif cap == 2:
        pp.namespace['stroke_cap'] = 'round'
    elif cap == 4:
        pp.namespace['stroke_cap'] = 'projecting'
    else:
        pp.namespace['stroke_cap'] = 'butt'


def stroke_weight(weight):
    pp = PyProcessing()
    pp.namespace['stroke_thickness'] = weight


def stroke_join(join):
    pp = PyProcessing()
    if join == 2:
        pp.namespace['stroke_join'] = 'round'
    elif join == 8:
        pp.namespace['stroke_join'] = 'miter'
    elif join == 32:
        pp.namespace['stroke_join'] = 'bevel'
    else:
        pp.namespace['stroke_join'] = 'bevel'
