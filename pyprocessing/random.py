import random as rd

import noise as noise_module


_octaves = 4
_persistence = 0.5
_lacunarity = 2


def noise(x, y=None, z=None):
    kwargs = {
        'octaves': _octaves,
        'persistence': _persistence,
        'lacunarity': _lacunarity,
    }
    if (y, z) == (None, None):
        return noise_module.pnoise1(x, **kwargs)
    if z is None:
        return noise_module.pnoise2(x, y, **kwargs)
    return noise_module.pnoise3(x, y, z, **kwargs)


def random_gaussian():
    return rd.gauss(0.0, 1.0)


def random_seed(seed):
    rd.seed(seed)


def random(low, high=None):
    if high is None:
        high = low
        low = 0.0
    return rd.uniform(low, high)


def noise_detail(lod, falloff=None, lacunarity=None):
    global _octaves
    _octaves = lod
    if falloff is not None:
        global _persistence
        _persistence = falloff
    if lacunarity is not None:
        global _lacunarity
        _lacunarity = lacunarity
