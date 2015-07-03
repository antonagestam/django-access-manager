from django.core.exceptions import ImproperlyConfigured

from .requirements import RequirementController


class ManagedAccessViewMixin(object):
    """
    Runs checks for requirements before running `dispatch` of the subclass.
    The subclass needs to specify `access_requirements` as an iterable of
    requirements.
    """

    access_requirements = None

    def get_access_requirements(self):
        if self.access_requirements is None:
            raise ImproperlyConfigured(
                "Views that extends ManagedAccessViewMixin need to specify "
                "`access_requirements` or implement a "
                "`get_access_requirements` method.")
        return self.access_requirements

    def dispatch(self, request, *args, **kwargs):
        requirements = self.get_access_requirements()
        controller = RequirementController(requirements)

        if not controller.control(request, args, kwargs):
            return controller.retval

        return super(ManagedAccessViewMixin, self).dispatch(
            request, *args, **kwargs)
