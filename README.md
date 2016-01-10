# Django Access Tools

[![Build Status](https://travis-ci.org/antonagestam/django-access-tools.svg?branch=master)](https://travis-ci.org/antonagestam/django-access-tools)
[![Coverage Status](https://coveralls.io/repos/antonagestam/django-access-tools/badge.svg?branch=coverage&service=github)](https://coveralls.io/github/antonagestam/django-access-tools?branch=coverage)

A tidy and extendable way of defining access requirements for views. Because mixins and decorators gets messy.

## Installation

Install using pip:

```
pip install django-access-tools
```

Or latest version in repo:

```
pip install -e git+https://github.com/antonagestam/django-access-tools/#egg=access
```

## Usage

### Requirements

Access requirements are specified by extending the `Requirement` class.
The `is_fulfilled` method is what defines your logic of when the requirement
is fulfilled. By overriding `not_fulfilled` you specify what should happen
if the requirement is not fulfilled. For example this simple `LoggedIn`
requirement:

```python
from django.http import Http404
from access.requirements import Requirement


class LoggedIn(Requirement):
    def is_fulfilled(self):
        return self.request.user.is_authenticated()
    
    def not_fulfilled(self):
        return Http404()
```

__`Requirement.request`:__ Request object. Gets set by `Requirement.setup`.

__`Requirement.args`:__ Request arguments passed to the view. Gets set by `Requirement.setup`.

__`Requirement.kwargs`:__ Request keyword arguments passed to the view. Gets set by `Requirement.setup`.


### Views

Access requirements for a view will be evaluated in the order they're specified.
For example `access_requirements = [LoggedIn, Active]` will have this chain of
events before the view is executed:

- Check if `LoggedIn.is_fulfilled()` is `True`.
- If not, make the view return `LoggedIn.not_fulfilled()` and stop.
- Otherwise, check if `Active.is_fulfilled()` is `True`
- If not, make the view return `Active.not_fulfilled()` and stop.
- Otherwise continue to execute the view as normal.

#### Class-based Views

Extend your views with `ManagedAccessViewMixin` and specify `access_requirements`:

```python
from django.views.generic import TemplateView
from access.views import ManagedAccessViewMixin
from access.requirements import Active, LoggedIn


class MyView(ManagedAccessViewMixin, TemplateView):
    access_requirements = [LoggedIn, Active]
    template = 'index.html'
```

#### Functional Views

For functional views, use `Requirement.as_decorator`.

```python
from access.requirements import LoggedIn

@LoggedIn.decorator
def my_view(request):
    return "Hello world"
```

When combining many requirements for a functional view, it's recommended to use
`access_requirements`. It returns a decorator and takes requirements as
positional arguments.

```python
from access.decorators import access_requirements
from access.requirements import Active, LoggedIn

@access_requirements(LoggedIn, Active)
def my_view(request):
    return "Hello world"
```

### Built-in Requirements

__`PageNotFoundRequirement(Requirement)`:__ Raises `Http404()` if unfulfilled.

__`Staff(PageNotFoundRequirement)`:__ Raises `Http404()` if user is not staff.

__`SuperUser(PageNotFoundRequirement)`:__ Raises `Http404()` if user is not superuser.

__`Active(PageNotFoundRequirement)`:__ Raises `Http404()` if user is not active.

__`RedirectRequirement(Requirement)`:__ Returns `Http307(self.get_url())` if not fulfilled.
Specify `url_name` or override `get_url` to set URL to redirect to. Appends the current URL
as ?next=current_url by default, set `append_next = False` to prevent this.

__`LoggedIn(RedirectRequirement)`:__ Returns `Http307('login')` if user is not authenticated.


### More Advanced Usage Example

Let's say you have a view where the user should only be allowed access
if they've accepted your terms of service and confirmed their email
address.

This example redirects the user to different views depending on if
they've accepted the terms of service and confirmed their email.
`RedirectRequirement` appends `?next={url}` to the redirect URLs
so that those views can redirect the user back after completing the
steps.

```python
from access.requirements import RedirectRequirement


class ProfileFieldRequirement(RedirectRequirement):
    profile_field_name = None

    def __init__(self, *args, **kwargs):
        self.required_field_value = kwargs.pop('required_field_value', True)
        super(ProfileFieldRequirement, self).__init__(*args, **kwargs)

    def is_fulfilled(self):
        if self.profile_field_name is None:
            raise ImproperlyConfigured(
                "ProfileFieldRequirements need to specify "
                "`profile_field_name`.")
        value = getattr(self.request.user.profile, self.profile_field_name)
        return value == self.required_field_value


class AcceptedTerms(ProfileFieldRequirement):
    url_name = 'accept_tos'
    profile_field_name = 'accepted_terms'


class ConfirmedEmail(ProfileFieldRequirement):
    url_name = 'prompt_email'
    profile_field_name = 'confirmed_email'

# … in your views.py:

from access.views import ManagedAccessViewMixin


class MyView(ManagedAccessViewMixin, View):
    access_requirements = [AcceptedTerms, ConfirmedEmail]
    
    # … view code
 
```


## Run tests

Install test requirements:

```
$ pip install -r test-requirements.txt
```

Run tests:

```
$ make test
```

## License

django-access-tools is licensed under The MIT License (MIT).
See [LICENSE file](./LICENSE) for more information.
