from urllib.parse import urlparse
import os, mimetypes
from mimetypes import guess_extension

# .htm causes a lot of wrong extension guessing
mimetypes.types_map.pop(".htm", None)
mimetypes.init(mimetypes.knownfiles+[os.path.abspath("extra_mime.types")])

class HttpMergeParameters(object):
    def process_request(self, request):
        if request.method.lower() == 'get':
            base = request.POST
            override = request.GET
        elif request.method.lower() == 'put':
            request.PUT = urlparse.parse_qs(request.body)
            base = request.PUT
            override = request.GET
        else:
            base = request.GET
            override = request.POST

        request.params = base.copy()
        request.params.update(override)


class HttpMethodOverride(object):
    def process_request(self, request):
        if 'HTTP_X_HTTP_METHOD' in request.META:  # (Microsoft)
            request.method = request.META['HTTP_X_HTTP_METHOD']
            return
        elif 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META:  # (Google/GData)
            request.method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE']
            return
        elif 'X_METHOD_OVERRIDE' in request.META:  # (IBM)
            request.method = request.META['X_METHOD_OVERRIDE']
            return
        elif 'X-Method' in request.params:  # custom
            request.method = request.params.get('X-Method')
            return


class ResponseFormatDetection(object):
    def process_request(self, request):
        expected = request.get_expected_mimetypes()
        ext = None
        mtype = None

        for mime in expected:
            ext = guess_extension(mime)
            if ext:
                mtype = mime
                break

        request.mime_ext = ext
        request.mime_type = mtype


class TemplateExtensionByAcceptedType(object):
    def process_template_response(self, request, response):
        ext = request.mime_ext
        mtype = request.mime_type

        if ext and request.resolver_match.app_name != 'admin':
            response['Content-Type'] = mtype + '; charset=' + response._charset
        else:
            ext = ''

        response.template_name += ext

        if request.is_pjax():
            path, filename = os.path.split(response.template_name)
            response.template_name = os.path.join(path, '_' + filename)

        return response
