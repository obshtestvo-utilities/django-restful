import json

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.conf import settings

from restful.exception.verbose import VerboseException, VerboseHtmlOnlyRedirectException
from restful.exception.htmlonlyredirect import HtmlOnlyRedirectException
from .http import HttpResponseNotModifiedRedirect


class ErrorHandler(object):
    def process_exception(self, request, exception):
        if isinstance(exception, HtmlOnlyRedirectException) and request.is_html():
            if isinstance(exception, VerboseException):
                messages.error(request, json.dumps({"generic": str(exception)}))
                for key, value in exception.get_errors().items():
                    messages.error(request, json.dumps({key: value}))
                messages.info(request, json.dumps({'input': request.params}))

            redirection = exception.get_redirect()
            return HttpResponseNotModifiedRedirect(resolve_url(redirection['name'], **redirection['vars']))

        template = getattr(settings, 'RESTFUL_ERROR_TEMPLATE', 'error/get')

        if not isinstance(exception, VerboseException):
            status = 403 if isinstance(exception, PermissionDenied) else 400
            return TemplateResponse(request, template, {"errors": {"generic": str(exception)}}, status=status)

        return TemplateResponse(request, template, {"errors": exception.get_errors()}, status=400)