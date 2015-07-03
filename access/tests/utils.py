from django.http import HttpResponseRedirect

from access.requirements import Requirement

successful_response = HttpResponseRedirect('lol')
unsuccessful_response = HttpResponseRedirect('woot')


class SuccessfulRequirement(Requirement):
    def is_fulfilled(self):
        return True


class UnSuccessfulRequirement(Requirement):
    def not_fulfilled(self):
        return unsuccessful_response

    def is_fulfilled(self):
        return False
