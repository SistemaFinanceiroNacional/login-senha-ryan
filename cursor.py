import condition

class linearCursor():

    def insert(self,values,into):
        listRegister = []
        with open(f"{into}.txt") as archive:
            register = {"saldo":0}
            fstr = f'{values["login"]}:{values["password"]}:0\n'
            archive.seek(0, 2)
            archive.write(fstr)
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

    def render(self,listAttributes):
        row = {}
        zipped = zip(listAttributes,self.cat.readlines())
        for (attributeValue,attributeDescription) in zipped:
            name,hasDefault,defaultValue = attributeDescription.split(":")
            if hasDefault == "true" and attributeValue == "":
                row[name] = defaultValue

            else:
                row[name] = attributeValue
        return row