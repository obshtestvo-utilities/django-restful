import pickle

from django.contrib import messages
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.conf import settings

from restful.exception.verbose import VerboseException, VerboseRedirectException
from restful.exception.http import HttpResponseNotModifiedRedirect


class ErrorHandler(object):
    def process_exception(self, request, exception):
        template = getattr(settings, 'RESTFUL_ERROR_TEMPLATE', 'error/get')

        if not isinstance(exception, VerboseException):
            return TemplateResponse(request, template, {"errors": {"generic": exception.messsage}}, status=400)

        if isinstance(exception, VerboseRedirectException):
            for key, value in exception.get_errors().iteritems():
                messages.error(request, pickle.dumps({key: value}))

            redirection = exception.get_redirect()
            return HttpResponseNotModifiedRedirect(resolve_url(redirection['name'], **redirection['vars']))

        if isinstance(exception, VerboseException):
            return TemplateResponse(request, template, {"errors": exception.get_errors()}, status=400)