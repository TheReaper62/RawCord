from .Functionals import *

class Emoji:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.roles = Okwargs['roles']
        self.user = Okwargs['user']
        self.require_colons = Okwargs['require_colons']
        self.managed = Okwargs['managed']
        self.animated = Okwargs['animated']
        self.available = Okwargs['available']
