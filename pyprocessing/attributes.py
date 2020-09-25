from pyprocessing import PyProcessing


def stroke_cap(cap):
    pp = PyProcessing()
    if cap == 1:
        pp.namespace['cap'] = 'butt'
    elif cap == 2:
        pp.namespace['cap'] = 'round'
    elif cap == 4:
        pp.namespace['cap'] = 'projecting'
    else:
        pp.namespace['cap'] = 'butt'


def stroke_weight(weight):
    pp = PyProcessing()
    pp.namespace['stroke_thickness'] = weight


def stroke_join(join):
    pp = PyProcessing()
    if join == 2:
        pp.namespace['join'] = 'round'
    elif join == 8:
        pp.namespace['join'] = 'miter'
    elif join == 32:
        pp.namespace['join'] = 'bevel'
    else:
        pp.namespace['join'] = 'bevel'
