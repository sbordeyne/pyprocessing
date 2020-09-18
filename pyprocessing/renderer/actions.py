class Action:
    def __init__(self, object, method, *args, **kwargs):
        self.object = object
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return getattr(self.object, self.method)(*self.args, **self.kwargs)
