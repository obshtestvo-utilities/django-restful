from django.core.exceptions import PermissionDenied
from .base import HttpException

class HtmlOnlyRedirectException(HttpException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redirect = {
            "name": None,
            "vars": {}
        }

    def get_redirect(self):
        return self.redirect

    def set_redirect(self, name, **kwargs):
        """
        @errors: {}
        Dictionary redirect's name and vars
        """
        self.redirect = {
            "name": name,
            "vars": kwargs
        }
        return self


class PermissionDeniedHtmlOnlyRedirectException(PermissionDenied, HtmlOnlyRedirectException):
    pass