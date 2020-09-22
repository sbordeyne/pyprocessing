import importlib.util
import tempfile

from pyprocessing import PyProcessing
from pyprocessing.renderer import TkRenderer


class Runner:
    renderers_mapping = {
        'TkRenderer': TkRenderer,
    }

    @classmethod
    def from_sketch_path(cls, sketch_path, **kwargs):
        spec = importlib.util.spec_from_file_location(
            "module.name", sketch_path,
        )
        sketch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sketch)
        return Runner(sketch, **kwargs)

    @classmethod
    def from_sketch_source(cls, sketch_source, **kwargs):
        with tempfile.NamedTemporaryFile('w') as tf:
            tf.write(sketch_source)
            return cls.from_sketch_path(tf.name, **kwargs)

    def __init__(self, sketch, renderers=None, logging_level=40):
        self.sketch = sketch
        if renderers is not None:
            renderers = [self.renderers_mapping[r] for r in renderers]
        if not renderers:
            renderers = [TkRenderer]
        self.renderers = renderers
        self.pp = PyProcessing()
        self.pp.logger.setLevel(logging_level)

        for renderer_class in self.renderers:
            self.pp.attach_renderer(renderer_class)

    def run(self):
        if 'setup' in dir(self.sketch):
            self.sketch.setup()
        self.pp.windows.setup()

        if 'draw' in dir(self.sketch):
            draw = self.sketch.draw
        else:
            def draw():
                return

        callables = {
            func_name: getattr(self.sketch, func_name)
            for func_name in dir(self.sketch)
            if callable(getattr(self.sketch, func_name))
        }

        self.pp.draw_fn = draw
        self.pp.callables.update(callables)
        self.pp.start()
