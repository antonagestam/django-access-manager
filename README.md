# Django Access Manager

[![Build Status](https://travis-ci.org/antonagestam/django-access-manager.svg?branch=master)](https://travis-ci.org/antonagestam/django-access-manager)

A tidy and extendable way of defining access requirements for views. Because mixins and decorators gets messy.

## Installation

Install using pip:

```
pip install django-access-manager
```

Or latest version in repo:

```
pip install -e git+https://github.com/FundedByMe/django-access-manager/#egg=access_manager
```

Add `'access_manager'` to your installed apps:

```python
INSTALLED_APPS += ('access_manager', )
```

## Usage

### Requirements

Access requirements are specified by extending the `BaseRequirement` class.
The `is_fulfilled` method is what defines your logic of when the requirement
is fulfilled. By overriding `not_fulfilled` you specify what should happen
if the requirement is not fulfilled. For example this simple `LoggedIn`
requirement:

```python
from django.http import Http404
from access_manager.requirements import BaseRequirement


class LoggedIn(BaseRequirement):
    def is_fulfilled(self):
        return self.request.user.is_authenticated()
    
    def not_fulfilled(self):
        return Http404()
```

__`BaseRequirement.request`:__ Request object. Gets set by `BaseRequirement.setup`.

__`BaseRequirement.args`:__ Request arguments passed to the view. Gets set by `BaseRequirement.setup`.

__`BaseRequirement.kwargs`:__ Request keyword arguments passed to the view. Gets set by `BaseRequirement.setup`.


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
from access_manager.views import ManagedAccessViewMixin
from access_manager.requirements import Active, LoggedIn


class MyView(ManagedAccessViewMixin, TemplateView):
    access_requirements = [LoggedIn, Active]
    template = 'index.html'
```

#### Functional Views

For functional views, `access_requirements` acts as a decorator and takes a
list of requirements as positional argument.

```python
from access_manager.decorators import access_requirements
from access_manager.requirements import Active, LoggedIn

@access_requirements([LoggedIn, Active])
def my_view(request):
    return "Hello world"
```

### Built-in Requirements

__`BasePageNotFoundRequirement(BaseRequirement)`:__ Raises `Http404()` if unfulfilled.

__`Staff(BasePageNotFoundRequirement)`:__ Raises `Http404()` if user is not staff.

__`SuperUser(BasePageNotFoundRequirement)`:__ Raises `Http404()` if user is not superuser.

__`Active(BasePageNotFoundRequirement)`:__ Raises `Http404()` if user is not active.

__`BaseRedirectRequirement(BaseRequirement)`:__ Returns `Http307(self.get_url())` if not fulfilled.
Specify `url_name` or override `get_url` to set URL to redirect to. Appends the current URL
as ?next=current_url by default, set `append_next = False` to prevent this.

__`LoggedIn(BaseRedirectRequirement)`:__ Returns `Http307('login')` if user is not authenticated.


### More Advanced Usage Example

Requiring a profile field to be `True` and redirecting if it's not.

```python
from access_manager.requirements import BaseRedirectRequirement


class BaseProfileFieldRequirement(BaseRedirectRequirement):
    profile_field_name = None

    def __init__(self, *args, **kwargs):
        self.required_field_value = kwargs.pop('required_field_value', True)
        super(BaseProfileFieldRequirement, self).__init__(*args, **kwargs)

    def is_fulfilled(self):
        if self.profile_field_name is None:
            raise ImproperlyConfigured(
                "ProfileFieldRequirements need to specify "
                "`profile_field_name`.")
        value = getattr(self.request.user.profile, self.profile_field_name)
        return value == self.required_field_value


class AcceptedTerms(BaseProfileFieldRequirement):
    url_name = 'accept_tos'
    profile_field_name = 'accepted_terms'


class ConfirmedEmail(BaseProfileFieldRequirement):
    url_name = 'prompt_email'
    profile_field_name = 'confirmed_email'

# … in your views.py:

from access_manager.views import ManagedAccessViewMixin


class MyView(ManagedAccessViewMixin, View):
    access_requirements = [AcceptedTerms, ConfirmedEmail]
    
    # … view code
 
```


## Run tests

Install test requirements:

```
$ pip install -r test_requirements.txt
```

Run tests:

```
$ make test
```

## License

django-access-manager is licensed under The MIT License (MIT).
See [LICENSE file](./LICENSE) for more information.
