from django.http.response import HttpResponseRedirectBase
from django.http.request import HttpRequest


class HttpResponseNotModifiedRedirect(HttpResponseRedirectBase):
    status_code = 303

# monkey-patching Django request, because we can't replace it with custom class
def is_pjax(self):
    return self.is_ajax() and (self.META.get('HTTP_X_PJAX') or self.params.get('X-Pjax'))

def is_html(self):
    return self.mime_ext == 'html'

def get_expected_mimetypes(self):
    header = self.META.get('HTTP_ACCEPT', '*/*')
    header = self.params.get('X-Accept', header)
    header_types = header.split(',')
    clean_types = []
    for mtype in header_types:
        mtype = mtype.strip()
        if mtype.find(';') > 0:
            mtype = mtype[0:mtype.find(';')]
        clean_types.append(mtype)

    return clean_types


HttpRequest.is_pjax = is_pjax
HttpRequest.get_expected_mimetypes = get_expected_mimetypes
HttpRequest.is_html = is_html