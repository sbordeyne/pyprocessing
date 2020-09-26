import datetime
import logging
import pathlib
import platform
import re
import sys
from time import time_ns

from pyprocessing.image import PImage
from pyprocessing.utils import SingletonMeta
from pyprocessing import frame_count  # noqa


hexcolor_re = re.compile(r'#\d{6}')


class PPNamespace(dict):
    attrdefault = {
        'framerate': 60,
        'stroke': '#000000',
        'fill': '#ffffff',
        'width': 640,
        'height': 480,
        'window_offset': (2, 2),
        'window_title': 'pyprocessing',
        'window_resizable': (False, False),
        'stroke_cap': 'round',
        'stroke_thickness': 1,
        'stroke_join': 'miter',
        'window_icon': PImage(
            (
                'base64:iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAc'
                'klEQVR4nJVSSQ7AIAgU0n8TXj4ebCiLkjpHnU2EAAwHIhoRicA9ux7SM'
                'rBTEbE7Va1RIcFTVdWLzZRPTQxLZuJM3VYSkVQvCFKTXOxPQgefkLwX9'
                'lNqcF3pAVDHemoPgEfZlh4Xb3iXyOz7//5ot+s9AZnvRP04a8+QAAAAA'
                'ElFTkSuQmCC'
            )
        )
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._changed_attrs = set()
        for k in self.attrdefault:
            setattr(self, '_' + k, self.attrdefault[k])

    def __getattr__(self, attr):
        if attr in self.attrdefault:
            return self.getattribute(attr)
        return super().__getattr__(attr)

    def __setitem__(self, item, value):
        if item in self.attrdefault:
            self._changed_attrs.add(item)
        return super().__setitem__(item, value)

    def getattribute(self, attr):
        def tocolor(value):
            if isinstance(value, str) and hexcolor_re.match(value):
                from pyprocessing.color import Color
                return Color.from_hex(value)
            return value

        if attr in self._changed_attrs:
            setattr(
                self, '_' + attr, tocolor(
                    self.get(
                        attr, self.attrdefault[attr],
                    )
                )
            )
            self._changed_attrs.discard(attr)
        return getattr(self, '_' + attr)


class RenderersDelegate:
    def __init__(self, pp, renderers, render_attr):
        self.pp = pp
        self.renderers = renderers
        self.render_attr = render_attr
        methods = (
            m
            for r in self.renderers
            for m in dir(getattr(r, render_attr))
            if not m.startswith('__')
        )
        for method in methods:
            if not hasattr(self, method):
                setattr(
                    self, method,
                    lambda *a, m=method, **kw: self.__delegate(
                        m, *a, **kw
                    )
                )

    def __delegate(self, mname, *args, **kwargs):
        self.pp.logger.debug(
            'Delegating to %s (*%s, **%s)', mname, args, kwargs
        )
        for r in self.renderers:
            getattr(getattr(r, self.render_attr), mname)(*args, **kwargs)


class PyProcessingCallables(dict):
    def __getattr__(self, attrname):
        if attrname in self.values():
            return self[attrname]
        super().__getattr__(attrname)

    def __getitem__(self, item):
        if item not in self:
            raise KeyError(
                f'Item {item} is not a callable. Is it defined properly?'
            )
        return super().__getitem__(item)


class PyProcessing(metaclass=SingletonMeta):
    def __init__(self):
        self.width = 640
        self.height = 480
        self.start_time_ns = 0
        self.namespace = PPNamespace()
        self._renderers = []
        self.callables = PyProcessingCallables()

        formatter = logging.Formatter(
            fmt=(
                '%(asctime)s-%(levelname)s:'
                '%(lineno)s | %(message)s'
            ),
            datefmt='%Y-%m-%dT%H:%M:%S,%f',
        )
        fhandler = logging.FileHandler(self._get_logs_path())
        fhandler.setFormatter(formatter)
        shandler = logging.StreamHandler(sys.stdout)
        shandler.setFormatter(formatter)
        self.logger = logging.getLogger('PyProcessing')
        self.logger.addHandler(fhandler)
        self.logger.addHandler(shandler)

    def _get_logs_path(self):
        system = platform.system()
        filename = f'{datetime.datetime.now().isoformat(sep="/")}-pyprocessing'
        filename = filename.replace(':', '-')
        path = None

        if system == 'Windows':
            path = pathlib.Path(
                    f'~/AppData/Local/PyProcessing/logs/{filename}.log'
                ).expanduser()
        if system == 'Darwin':
            path = pathlib.Path(
                    f'~/.pyprocessing/logs/{filename}.log'
                ).expanduser()
        if system == 'Linux':
            path = pathlib.Path(
                    f'~/.pyprocessing/{filename}.log'
                ).expanduser()

        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            return str(path)

    def attach_renderer(self, renderer_class):
        renderer = renderer_class(self)
        renderer.init()
        self._renderers.append(renderer)

    def start(self):
        for renderer in self._renderers:
            renderer.start()
        self.start_time_ns = time_ns()

    @property
    def windows(self):
        return RenderersDelegate(self, self._renderers, 'window')

    @property
    def renderers(self):
        return RenderersDelegate(self, self._renderers, 'this')

    def draw(self):
        global frame_count
        if hasattr(self, 'draw_fn'):
            self.draw_fn()
        frame_count += 1
