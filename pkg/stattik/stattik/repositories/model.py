import grotto.ogm

# NOTE: Stattik's models get their own grotto schema, so their labels (Page, Post, ...) can't clash with other models in the process
SCHEMA = grotto.ogm.Schema("stattik")

class Model(grotto.ogm.Model):
    __abstract__ = True
    __schema__ = SCHEMA

    def __getattr__(self, name):
        # NOTE: Undeclared front matter lives in extras.  Expose it as attributes so templates can read page.whatever
        if name.startswith("__") or name == "extras":
            raise AttributeError(name)
        try:
            return self.extras[name]
        except KeyError:
            raise AttributeError(name) from None
