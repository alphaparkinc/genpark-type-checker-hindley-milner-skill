"""Hindley-Milner Type Inference Engine (Algorithm W)
100% Python Standard Library.
"""

class TypeVar:
    def __init__(self, name):
        self.name = name
        self.instance = None

    def __repr__(self):
        if self.instance:
            return repr(self.instance)
        return self.name

class TypeOperator:
    def __init__(self, name, types):
        self.name = name
        self.types = types

    def __repr__(self):
        if len(self.types) == 0:
            return self.name
        elif len(self.types) == 2 and self.name == "->":
            return f"({self.types[0]} -> {self.types[1]})"
        return f"{self.name} [{' '.join(map(repr, self.types))}]"

class HMTypeInference:
    """Algorithm W unification solver."""
    def prune(self, t):
        if isinstance(t, TypeVar):
            if t.instance is not None:
                t.instance = self.prune(t.instance)
                return t.instance
        return t

    def unify(self, t1, t2):
        a = self.prune(t1)
        b = self.prune(t2)
        if isinstance(a, TypeVar):
            if a != b:
                if self.occurs_in_type(a, b):
                    raise TypeError("Type error: recursive unification")
                a.instance = b
            return
        if isinstance(b, TypeVar):
            self.unify(b, a)
            return
        if isinstance(a, TypeOperator) and isinstance(b, TypeOperator):
            if a.name != b.name or len(a.types) != len(b.types):
                raise TypeError(f"Type mismatch: {a.name} vs {b.name}")
            for p1, p2 in zip(a.types, b.types):
                self.unify(p1, p2)
            return
        raise TypeError("Cannot unify")

    def occurs_in_type(self, v, t):
        t = self.prune(t)
        if t == v:
            return True
        elif isinstance(t, TypeOperator):
            return any(self.occurs_in_type(v, p) for p in t.types)
        return False
