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
