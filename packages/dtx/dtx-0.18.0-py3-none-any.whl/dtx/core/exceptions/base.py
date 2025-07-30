class FeatureNotImplementedError(ValueError):
    pass


class MethodNotImplementedError(FeatureNotImplementedError):
    pass


class ModuleNotFound(FeatureNotImplementedError):
    pass


class EntityNotFound(ValueError):
    pass
