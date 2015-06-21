from .requirements import RequirementController


def access_requirements(fn, requirements):
    controller = RequirementController(requirements)

    def wrapper(request, *args, **kwargs):
        if not controller.control(request, args, kwargs):
            return controller.retval
        return fn(request, *args, **kwargs)
    return wrapper
