import condition

class linearCursor():

    def insert(self,values,into):
        listRegister = []
        with open(f"{into}.txt") as archive, catalog(into) as cat:
            archive.seek(0, 2)
            archive.write()
            register.update(values)
            listRegister = [register]
        return listRegister



    def select(self,columns,fromTable,where):
        listRegister = []
        with open(f"{fromTable}.txt") as archive,catalog(fromTable) as cat:
            archive.seek(0)
            for line in archive:
                line = line[:-1]
                attributes = line.split(":")
                register = cat.render(attributes)
                if where.match(register):
                    listRegister.append(condition.projectioncolumns(columns).proj(register))

        return listRegister

class catalog:
    def __init__(self,table):
        self.cat = open(f"{table}.cat")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cat.close()

    def render(self,dicioAttributes):

        class column:
            def __init__(self, listSplited):
                self.name, self.hasDefault, self.defaultValue, self.type = listSplited

            def validate(self, value):
                pass

        row = []
        lineRead = map(lambda l: column(l.split(":")),self.cat.readlines())

        for i in lineRead:
            if i.validate(dicioAttributes):
                row.append((i.type, dicioAttributes[i.name]))

            else:
                return []

        return row