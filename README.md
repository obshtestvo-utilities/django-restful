## django-restful

### What this does
A module that provides REST-ful way to interact with views, templates, response types,
request parameters and query generation in templates. It also provides an easy way to handle all errors
in one place.

Comes with:

 - middleware that merges all request parameters in `request.params`
 - middleware that allows you to fake/force http method via http parameter (...) or http header (...)
 - decorator for automatic template name detection (via class name and method name or via passed parameters to the decorator).
 Same decorator eases passing data and setting status code by allowing
 - custom exceptions for verbose description of errors
 - middleware that handles all exceptions and either:
   1. passes errors to to a single error template
   1. redirects to route you've provided and passes errors as session messages

### What this doesn't do
 1. It doesn't offer or forces you to use serializers. You transform the data yourself, you output the data in templates.
 It only offers a `json` template helper which can be useful when you've prepared a dict.
 1. It doesn't take care of pagination for you.

### Installation & Configuration

```sh
pip install django-restful
```

The package provides few middleware classes that do **the magic**:

 1. `django.middleware.common.HttpMergeParameters`
 1. `django.middleware.common.HttpMethodOverride`
 1. `django.middleware.common.ErrorHandler`
 1. `django.middleware.common.ResponseFormatDetection`

In `settings.py`:

```py
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'restful.middleware.HttpMergeParameters',
    'restful.middleware.HttpMethodOverride',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Before using CSRF make sure it's ONLY enabled when user is logging in or already logged in via cookies
    # Make sure it's not enabled for RESTful requests authenticated via Basic, Digest or OAuth
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'restful.error_handler.ErrorHandler',
    'restful.middleware.ResponseFormatDetection',
)
```


### Example

```py
from django.views.generic.base import View
from restful.decorators import restful_view_templates

from models import User


@restful_view_templates
class UserView(View):
    def get(self, request):
        return {
            "page": "inner about",
        }

    def post(self, request, id):
        user = User.objects.get(pk=id)
        user.. #todo: finish

```