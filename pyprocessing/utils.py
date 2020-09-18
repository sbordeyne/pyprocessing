def int_to_color(color):
    assert isinstance(color, int), 'Color should be an int.'

    h = hex(color)[2:]
    return f'#{h.zfill(2) * 3}'


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
