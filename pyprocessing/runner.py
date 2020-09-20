import importlib.util
import tempfile

from pyprocessing import PyProcessing
from pyprocessing.renderer import TkRenderer


class Runner:
    renderers_mapping = {
        'TkRenderer': TkRenderer,
    }

    @classmethod
    def from_sketch_path(cls, sketch_path, renderers=None):
        spec = importlib.util.spec_from_file_location(
            "module.name", sketch_path,
        )
        sketch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sketch)
        return Runner(sketch, renderers=renderers)

    @classmethod
    def from_sketch_source(cls, sketch_source, renderers=None):
        with tempfile.NamedTemporaryFile('w') as tf:
            tf.write(sketch_source)
            return cls.from_sketch_path(tf.name, renderers=renderers)

    def __init__(self, sketch, renderers=None):
        self.sketch = sketch
        if renderers is not None:
            renderers = [self.renderers_mapping[r] for r in renderers]
        if not renderers:
            renderers = [TkRenderer]
        self.renderers = renderers

        self.pp = PyProcessing()

    def run(self):
        if 'setup' in dir(self.sketch):
            self.sketch.setup()

        if 'draw' in dir(self.sketch):
            draw = self.sketch.draw
        else:
            def draw():
                return

        self.pp.draw = draw

        for renderer_class in self.renderers:
            self.pp.attach_renderer(renderer_class)

        self.pp.start()
