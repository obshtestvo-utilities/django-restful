import json
from .htmlonlyredirect import HtmlOnlyRedirectException
from .base import HttpException

class VerboseException(HttpException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = {}

    def get_errors(self):
        compact_errors = {}
        for topic, errors in self.errors.items():
            if len(errors) == 1:
                compact_errors[topic] = errors[0]
            else:
                compact_errors[topic] = errors
        return compact_errors

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