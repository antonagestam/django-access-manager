from django.test import TestCase
from django.http import HttpResponseRedirect
from django.views.generic import View

from .views import ManagedAccessViewMixin
from .requirements import BaseRequirement
from .decorators import access_requirements

successful_response = HttpResponseRedirect('lol')
unsuccessful_response = HttpResponseRedirect('woot')


class SuccessfulRequirement(BaseRequirement):
    def is_fulfilled(self):
        return True


class UnSuccessfulRequirement(BaseRequirement):
    def not_fulfilled(self):
        return unsuccessful_response

    def is_fulfilled(self):
        return False


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


def test_view(request, *args, **kwargs):
    test_view.dispatch_called = True
    return successful_response


class TestAccessRequirementsDecorator(TestCase):
    def setUp(self):
        self.request = {}
        test_view.dispatch_called = False

    def test_successfull(self):
        first = SuccessfulRequirement()
        second = SuccessfulRequirement()
        view = access_requirements(first, second)(test_view)
        result = view(self.request)
        self.assertTrue(test_view.dispatch_called)
        self.assertEqual(result, successful_response)

    def test_first_unfulfilled(self):
        first = UnSuccessfulRequirement()
        second = SuccessfulRequirement()
        view = access_requirements(first, second)(test_view)
        result = view(self.request)
        self.assertFalse(test_view.dispatch_called)
        self.assertEqual(result, unsuccessful_response)

    def test_second_unfulfilled(self):
        first = SuccessfulRequirement()
        second = UnSuccessfulRequirement()
        view = access_requirements(first, second)(test_view)
        result = view(self.request)
        self.assertFalse(test_view.dispatch_called)
        self.assertEqual(result, unsuccessful_response)
