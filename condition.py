class condition():
    def __str__(self):
        raise NotImplementedError

    def match(self, dicio):
        raise NotImplementedError

class andCondition(condition):
    def __init__(self, cond1, cond2):
        self.cond1 = cond1
        self.cond2 = cond2

    def __str__(self):
        return f"{self.cond1} and {self.cond2}"

    def match(self, dicio):
        return self.cond1.match(dicio) and self.cond2.match(dicio)

class equal(condition):
    def __init__(self, projection1, projection2):
        self.projection1 = projection1
        self.projection2 = projection2

    def __str__(self):
        return f"{self.projection1} == {self.projection2}"

    def match(self, dicio):
        return self.projection1.proj(dicio) == self.projection2.proj(dicio)


class projection():
    def proj(self,dicio):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

class literal(projection):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return f"'{self.string}'"

    def proj(self,dicio):
        return self.string

def columnname(x):
    return projectioncolumns([x])

class projectioncolumns(projection):
    def __init__(self,columns):
        self.columns = columns

    def __str__(self):
        def putQuotes(str):
            return f'"{str}"'

        listColumns = map(putQuotes,self.columns)
        x = ",".join(listColumns)
        return x

    def proj(self,dicio):
        returnDict = {}
        if self.columns == ["*"]:
            returnDict = dicio

        else:
            for i in self.columns:
                returnDict[i] = dicio[i]
        return returnDict