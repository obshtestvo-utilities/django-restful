from ..http import get_exception_status_code

class HttpException(Exception):

    def by(self, exception):
        self.status_code = get_exception_status_code(exception)
