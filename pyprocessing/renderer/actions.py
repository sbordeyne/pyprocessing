class Action:
    def __init__(self, object, method, *args, **kwargs):
        self.object = object
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return getattr(self.object, self.method)(*self.args, **self.kwargs)

    def __str__(self):
        return (
            f'A({self.object.__class__.__name__}, {self.method})'
            f'({self.args}, {self.kwargs}'
        )
