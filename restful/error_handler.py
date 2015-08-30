import json

from django.contrib import messages
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.conf import settings

from restful.exception.verbose import VerboseException
from restful.exception.htmlonlyredirect import HtmlOnlyRedirectException
from .http import HttpResponseNotModifiedRedirect, get_exception_status_code
from .signals import pre_error_rendering


class ErrorHandler(object):

    def process_exception(self, request, exception):
        status = get_exception_status_code(exception)

        if isinstance(exception, HtmlOnlyRedirectException) and request.is_html() and not request.is_pjax():
            if isinstance(exception, VerboseException):
                messages.error(request, json.dumps({"generic": str(exception)}))
                for key, value in exception.get_errors().items():
                    messages.error(request, json.dumps({key: value}))
                last_input = request.params.copy()
                try:
                    del last_input["csrfmiddlewaretoken"]
                except:
                    pass
                messages.info(request, json.dumps({'input': last_input}))

            redirection = exception.get_redirect()
            return HttpResponseNotModifiedRedirect(resolve_url(redirection['name'], **redirection['vars']))

        if isinstance(exception, VerboseException):
            errors = exception.get_errors()
        else:
            errors = {"generic": str(exception)}

        template_alternatives = pre_error_rendering.send(
            sender=ErrorHandler,
            url_name=request.resolver_match.url_name,
            request=request,
            errors=errors
        )
        template = getattr(settings, 'RESTFUL_ERROR_TEMPLATE', 'error/get')
        for receiver, template_name in template_alternatives:
            if template_name is not None:
                template = template_name
                break

        return TemplateResponse(request, template, {"errors": errors}, status=status)