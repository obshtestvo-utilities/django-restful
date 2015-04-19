import json

from django.contrib import messages
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.conf import settings

from restful.exception.verbose import VerboseException, VerboseHtmlOnlyRedirectException
from .http import HttpResponseNotModifiedRedirect


class ErrorHandler(object):
    def process_exception(self, request, exception):
        if isinstance(exception, VerboseHtmlOnlyRedirectException):
            if request.is_html():
                for key, value in exception.get_errors().items():
                    messages.error(request, json.dumps({key: value}))

                redirection = exception.get_redirect()
                return HttpResponseNotModifiedRedirect(resolve_url(redirection['name'], **redirection['vars']))

        template = getattr(settings, 'RESTFUL_ERROR_TEMPLATE', 'error/get')

        if not isinstance(exception, VerboseException):
            return TemplateResponse(request, template, {"errors": {"generic": str(exception)}}, status=400)

        if isinstance(exception, VerboseException):
            return TemplateResponse(request, template, {"errors": exception.get_errors()}, status=400)