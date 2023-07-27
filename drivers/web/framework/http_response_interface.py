class HttpResponseInterface:
    def get_headers(self):
        raise NotImplementedError

    def get_body(self):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError
