from django.test import TestCase
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured

from access.views import ManagedAccessViewMixin

from .utils import (
    SuccessfulRequirement, UnSuccessfulRequirement, successful_response,
    unsuccessful_response)


class TestView(View):
    dispatch_called = False

    def dispatch(self, *args, **kwargs):
        self.dispatch_called = True
        return successful_response


class FakeView(ManagedAccessViewMixin, TestView):
    pass


class TestManagedAccessViewMixin(TestCase):
    def setUp(self):
        self.view = FakeView()
        self.request = {}

    def test_successful(self):
        first = SuccessfulRequirement()
        second = SuccessfulRequirement()
        self.view.access_requirements = [first, second]
        result = self.view.dispatch(self.request)
        self.assertTrue(self.view.dispatch_called)
        self.assertEqual(result, successful_response)

    def test_first_unfulfilled(self):
        first = UnSuccessfulRequirement()
        second = SuccessfulRequirement()
        self.view.access_requirements = [first, second]
        result = self.view.dispatch(self.request)
        self.assertFalse(self.view.dispatch_called)
        self.assertEqual(result, unsuccessful_response)

    def test_second_unfulfilled(self):
        first = SuccessfulRequirement()
        second = UnSuccessfulRequirement()
        self.view.access_requirements = [first, second]
        result = self.view.dispatch(self.request)
        self.assertFalse(self.view.dispatch_called)
        self.assertEqual(result, unsuccessful_response)

    def test_get_access_requirements(self):
        with self.assertRaises(ImproperlyConfigured):
            self.view.get_access_requirements()
        self.view.access_requirements = []
