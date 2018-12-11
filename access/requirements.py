from functools import wraps

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.http import Http404

from .http import Http307


class Requirement(object):
    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def is_fulfilled(self):
        raise ImproperlyConfigured(
            "Requirements need to implement a `is_fulfilled` method.")

    def not_fulfilled(self):
        raise ImproperlyConfigured(
            "Requirements need to implement a `not_fulfilled` method.")

    def decorator(self, fn):
        controller = RequirementController([self])

        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            if not controller.control(request, args, kwargs):
                return controller.retval
            return fn(request, *args, **kwargs)
        return wrapper


class PageNotFoundRequirement(Requirement):
    def not_fulfilled(self):
        raise Http404()


class Staff(PageNotFoundRequirement):
    def is_fulfilled(self):
        return self.request.user.is_staff


class SuperUser(PageNotFoundRequirement):
    def is_fulfilled(self):
        return self.request.user.is_superuser


class Active(PageNotFoundRequirement):
    def is_fulfilled(self):
        return self.request.user.is_active


class RedirectRequirement(Requirement):
    url_name = None
    append_next = True

    def get_url_args(self):
        return []

    def get_url_name(self):
        if self.url_name is None:
            raise ImproperlyConfigured(
                "You need to specify `url_name` or override the `get_url_name` "
                "method.")
        return self.url_name

    def get_url(self):
        url = reverse(self.get_url_name(), args=self.get_url_args())
        if self.append_next:
            url += "?next=%s" % self.request.get_full_path()
        return url

    def not_fulfilled(self):
        return Http307(self.get_url())


class LoggedIn(RedirectRequirement):
    url_name = 'login'

    def is_fulfilled(self):
        return self.request.user.is_authenticated


class RequirementController(object):
    """
    Encapsulates logic for checking if requirements are fulfilled.
    See views.ManagedAccessViewMixin.dispatch and decorators.access_requirements
    for example implementations.
    """
    def __init__(self, requirements):
        self.requirements = requirements
        self.retval = None

    def control(self, request, args, kwargs):
        for requirement in self.requirements:
            requirement.setup(request, *args, **kwargs)
            if not requirement.is_fulfilled():
                self.retval = requirement.not_fulfilled()
                return False
        return True
