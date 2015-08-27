import os
import importlib
import json
from functools import wraps

from django.utils.decorators import available_attrs
from django.views.generic.base import View
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.conf import settings
from django.contrib import messages
from django.shortcuts import resolve_url

from .http import HtmlOnlyRedirectSuccessDict, HttpResponseNotModifiedRedirect
from .signals import pre_success_rendering

response_class = getattr(settings, 'RESTFUL_RESPONSE', 'django.template.response.TemplateResponse')
response_class = response_class.rsplit('.', 1)
response_class = getattr(importlib.import_module(response_class[0]), response_class[1])

def restful_template(dirname, name, appname=None, func=None):
    def decorator(action):
        # maintain correct stacktrace name and doc
        @wraps(action, assigned=available_attrs(action))
        def _restful(obj, request, *args, **kwargs):
            template = os.path.join(dirname, name)
            try:
                get_template(template + request.mime_ext)
            except TemplateDoesNotExist:
                if appname is not None:
                    template = os.path.join(appname, template)
            data = action(obj, request, *args, **kwargs)

            template_alternatives = pre_success_rendering.send(
                sender=obj.__class__,
                url_name=request.resolver_match.url_name,
                params=request.params,
                data=data,
                http_verb=name
            )
            for receiver, template_name in template_alternatives:
                if template_name is not None:
                    template = template_name
                    break

            if isinstance(data, HtmlOnlyRedirectSuccessDict) and request.is_html() and not request.is_pjax():
                for key, value in data.items():
                    messages.success(request, json.dumps({key: value}))

                redirection = data.get_redirect()
                return HttpResponseNotModifiedRedirect(resolve_url(redirection['name'], **redirection['vars']))

            if not (isinstance(data, (tuple, dict)) or data is None):
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
    for verb in View.http_method_names:
        if hasattr(cls, verb):
            appname = cls.__module__.split('.')[0]
            viewname = cls.__name__[:-4].lower()
            setattr(cls, verb, restful_template(viewname, verb, appname=appname, func=getattr(cls, verb)))
    return cls
