import datetime
import logging
import pathlib
import platform
import sys
from time import time_ns

from pyprocessing.utils import SingletonMeta


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


class PyProcessing(metaclass=SingletonMeta):
    def __init__(self):
        self.width = 640
        self.height = 480
        self.start_time_ns = 0
        self.namespace = {}
        self.renderers = []

        formatter = logging.Formatter('%(asctime)s - %(levelinfo)s : %(message)s')
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
                    f'~/PyProcessing/logs/{filename}.log'
                ).expanduser()
        if system == 'Linux':
            path = pathlib.Path(
                    f'~/pyprocessing/{filename}.log'
                ).expanduser()

        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            return str(path)

    def attach_renderer(self, renderer_class):
        renderer = renderer_class(self)
        renderer.init()
        self.renderers.append(renderer)

    def start(self):
        for renderer in self.renderers:
            renderer.start()
        self.start_time_ns = time_ns()

    @property
    def windows(self):
        return RenderersDelegate(self, self.renderers, 'window')
