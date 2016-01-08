from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured

from access.requirements import (
    Staff, SuperUser, LoggedIn, Active, Requirement, RequirementController,
    PageNotFoundRequirement)
from access.factories import UserFactory, InActiveUserFactory


class TestRequirements(TestCase):
    request = None

    def setUp(self):
        self.request = None

    def set_request(self, **kwargs):
        self.request = HttpRequest()
        for k, v in kwargs.items():
            setattr(self.request, k, v)

    def assert_requirement_fulfilled(self, requirement):
        requirement.setup(self.request)
        self.assertTrue(
            requirement.is_fulfilled(), msg="The requirement is not fulfilled")

    def assert_requirement_unfulfilled(self, requirement):
        requirement.setup(self.request)
        self.assertFalse(
            requirement.is_fulfilled(), msg="The requirement is fulfilled")

    def test_requirement(self):
        with self.assertRaises(ImproperlyConfigured):
            Requirement().is_fulfilled()
        with self.assertRaises(ImproperlyConfigured):
            Requirement().not_fulfilled()

    def test_staff(self):
        user = UserFactory.build(is_staff=False)
        self.set_request(user=user)
        self.assert_requirement_unfulfilled(Staff())

        user.is_staff = True
        self.assert_requirement_fulfilled(Staff())

    def test_superuser(self):
        user = UserFactory.build(is_superuser=False)
        self.set_request(user=user)
        self.assert_requirement_unfulfilled(SuperUser())

        user.is_superuser = True
        self.assert_requirement_fulfilled(SuperUser())

    def test_active(self):
        user = InActiveUserFactory.build()
        self.set_request(user=user)
        self.assert_requirement_unfulfilled(Active())

        user.is_active = True
        self.assert_requirement_fulfilled(Active())

    def test_logged_in(self):
        self.set_request(user=AnonymousUser())
        self.assert_requirement_unfulfilled(LoggedIn())

        self.set_request(user=UserFactory.build())
        self.assert_requirement_fulfilled(LoggedIn())

    def test_page_not_found(self):
        with self.assertRaises(Http404):
            PageNotFoundRequirement().not_fulfilled()


class SuccessfulRequirement(Requirement):
    not_fulfilled_called = False
    is_fulfilled_called = False
    response_obj = HttpResponseRedirect('lol')

    def not_fulfilled(self):
        self.not_fulfilled_called = True
        return self.response_obj

    def is_fulfilled(self):
        self.is_fulfilled_called = True
        return True


class UnSuccessfulRequirement(SuccessfulRequirement):
    def is_fulfilled(self):
        self.is_fulfilled_called = True
        return False


class TestRequirementController(TestCase):
    def test_successfull(self):
        first = SuccessfulRequirement()
        second = SuccessfulRequirement()
        controller = RequirementController([first, second])
        result = controller.control({}, [], {})
        self.assertTrue(result)
        self.assertTrue(first.is_fulfilled_called)
        self.assertTrue(second.is_fulfilled_called)

    def test_first_unfulfilled(self):
        first = UnSuccessfulRequirement()
        second = SuccessfulRequirement()
        controller = RequirementController([first, second])
        result = controller.control({}, [], {})
        self.assertFalse(result)
        self.assertTrue(first.is_fulfilled_called)
        self.assertTrue(first.not_fulfilled_called)
        self.assertFalse(second.is_fulfilled_called)
        self.assertEqual(controller.retval, first.response_obj)

    def test_second_unfulfilled(self):
        first = SuccessfulRequirement()
        second = UnSuccessfulRequirement()
        controller = RequirementController([first, second])
        result = controller.control({}, [], {})
        self.assertFalse(result)
        self.assertTrue(first.is_fulfilled_called)
        self.assertFalse(first.not_fulfilled_called)
        self.assertTrue(second.is_fulfilled_called)
        self.assertTrue(second.not_fulfilled_called)
        self.assertEqual(controller.retval, second.response_obj)
