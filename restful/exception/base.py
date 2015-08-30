class HttpException(Exception):

    def by(self, exception):
        try:
            self.status_code = exception.status_code
        except:
            pass
        return self