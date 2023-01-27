class maybe:
    def map(self,function):
        raise NotImplementedError

    def orElse(self,default):
        raise NotImplementedError

    def orElseThrow(self, value):
        raise NotImplementedError

class just(maybe):
    def __init__(self,value):
        self.value = value

    def map(self, function):
        return just(function(self.value))

    def orElse(self, default):
        return self.value

    def orElseThrow(self, value):
        return self.value

class nothing(maybe):

    def map(self, function):
        return self

    def orElse(self, default):
        return default()

    def orElseThrow(self, value):
        raise value

def getFirstNotEmpty(possible_not_empties):
    for possible in possible_not_empties:
        if isinstance(possible, just):
            return possible
    return nothing()