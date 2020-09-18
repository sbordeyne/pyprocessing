from pyprocessing.utils import SingletonMeta


class RenderersDelegate:
    def __init__(self, renderers, render_attr):
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
        print(mname, args, kwargs)
        for r in self.renderers:
            getattr(getattr(r, self.render_attr), mname)(*args, **kwargs)


class PyProcessing(metaclass=SingletonMeta):
    def __init__(self):
        self.width = 640
        self.height = 480
        self.namespace = {}
        self.renderers = []

    def attach_renderer(self, renderer_class):
        renderer = renderer_class(self)
        renderer.init()
        self.renderers.append(renderer)

    def start(self):
        for renderer in self.renderers:
            renderer.start()

    @property
    def windows(self):
        return RenderersDelegate(self.renderers, 'window')
