from django.test import TestCase

from access.decorators import access_requirements

from .utils import (
    SuccessfulRequirement, UnSuccessfulRequirement, successful_response,
    unsuccessful_response)


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


class TestAsDecorator(TestCase):
    def setUp(self):
        self.request = {}
        test_view.dispatch_called = False

    def test_successful(self):
        first = SuccessfulRequirement()
        second = SuccessfulRequirement()
        view = second.decorator(first.decorator(test_view))
        result = view(self.request)
        self.assertTrue(test_view.dispatch_called)
        self.assertEqual(result, successful_response)

    def test_first_unfulfilled(self):
        first = UnSuccessfulRequirement()
        second = SuccessfulRequirement()
        view = second.decorator(first.decorator(test_view))
        result = view(self.request)
        self.assertFalse(test_view.dispatch_called)
        self.assertEqual(result, unsuccessful_response)

    def test_second_unfulfilled(self):
        first = SuccessfulRequirement()
        second = UnSuccessfulRequirement()
        view = second.decorator(first.decorator(test_view))
        result = view(self.request)
        self.assertFalse(test_view.dispatch_called)
        self.assertEqual(result, unsuccessful_response)
