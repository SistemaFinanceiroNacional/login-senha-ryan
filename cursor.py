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
        with open(f"{fromTable}.txt") as archive:
            archive.seek(0)
            for line in archive:
                line = line[:-1]
                logindoc, passworddoc, saldo = line.split(":")
                register = {"login":logindoc,"password":passworddoc, "saldo":saldo}
                if where.match(register):
                    listRegister.append(condition.projectioncolumns(columns).proj(register))

        return listRegister

class catalog:
    def __init__(self):
        pass
