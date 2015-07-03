from functools import wraps

from .requirements import RequirementController


def access_requirements(*requirements):
    controller = RequirementController(requirements)

    def decorator(fn):
        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            if not controller.control(request, args, kwargs):
                return controller.retval
            return fn(request, *args, **kwargs)
        return wrapper
    return decorator
