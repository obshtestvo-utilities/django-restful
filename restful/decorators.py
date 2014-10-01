import os
import importlib
import inspect
from functools import wraps

from django.utils.decorators import available_attrs
from django.views.generic.base import View
from django.conf import settings

response_class = settings.RESTFUL_RESPONSE if hasattr(settings, 'RESTFUL_RESPONSE') else 'django.template.response.TemplateResponse'
response_class = response_class.rsplit('.', 1)
response_class = getattr(importlib.import_module(response_class[0]), response_class[1])

def restful_template(dirname, name, func=None):
    def decorator(action):
        # maintain correct stacktrace name and doc
        @wraps(action, assigned=available_attrs(action))
        def _restful(obj, request, *args, **kwargs):
            template = os.path.join(dirname, name)
            data = action(obj, request, *args, **kwargs)
            if not (isinstance(data, tuple) or isinstance(data, dict) or data is None):
                return data
            status = 200
            if isinstance(data, tuple):
                status = data[1]
                data = data[0]
            return response_class(request, template, data, status=status)

        return _restful

    if func:
        return decorator(func)

    return decorator


def restful_view_templates(cls):
    for name, m in inspect.getmembers(cls, inspect.ismethod):
        if name in View.http_method_names:
            setattr(cls, name, restful_template(cls.__name__[:-4].lower(), name, func=m))
    return cls
