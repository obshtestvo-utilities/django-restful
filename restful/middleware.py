from urllib.parse import urlparse
import os, mimetypes
from mimetypes import guess_extension

# .htm causes a lot of wrong extension guessing
mimetypes.types_map.pop(".shtml", None)
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
        try:
            request.method = request.META['HTTP_X_HTTP_METHOD']  # (Microsoft)
            return
        except:
            pass
        try:
            request.method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE']  # (Google/GData)
            return
        except:
            pass
        try:
            request.method = request.META['X_METHOD_OVERRIDE']  # (IBM)
            return
        except:
            pass
        try:
            request.method = request.params['X-Method']  # custom
            return
        except:
            pass


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
