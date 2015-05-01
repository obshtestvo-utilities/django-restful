import json
from .htmlonlyredirect import HtmlOnlyRedirectException

class VerboseException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = {}

    def get_errors(self):
        return self.errors

    def set_errors(self, errors):
        """
        @errors: {}
        Dictionary of errors
        """
        self.errors = errors
        return self

    def add_error(self, name, message):
        try:
            self.errors[name]
        except:
            self.errors[name] = []
        self.errors[name].append(message)
        return self

    def __str__(self):
        return json.dumps(self.errors)


class VerboseHtmlOnlyRedirectException(VerboseException, HtmlOnlyRedirectException):
    pass