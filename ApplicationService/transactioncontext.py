class transactioncontext:
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def get_errors(self):
        raise NotImplementedError
