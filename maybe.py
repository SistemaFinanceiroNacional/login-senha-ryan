class maybe():
    def map(self,function):
        raise NotImplementedError

    def orElse(self,default):
        raise NotImplementedError


class just(maybe):
    def __init__(self,value):
        self.value = value

    def map(self,function):
        return just(function(self.value))

    def orElse(self,default):
        return self.value


class nothing(maybe):

    def map(self,function):
        return self

    def orElse(self,default):
        return default()