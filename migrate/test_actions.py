import actions
import filemockFormigrations
import pathlib

class fakeCursor:
    def __init__(self):
        self.outputList = []

    def execute(self, string):
        self.outputList.append(string)


def test_unappliedMigrations_1():
    fMigrations = ["file1.sql", "file2.sql", "file3.sql", "file4.sql", "file5.sql", "file6.sql", "file7.sql"]
    DBMigrations = ["file1.sql", "file2.sql", "file3.sql", "file4.sql", "file5.sql", "file6.sql"]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert notUsedMigrations == ["file7.sql"]

def test_unappliedMigrations_2():
    fMigrations = ["file1.sql", "file2.sql", "file3.sql", "file4.sql", "file5.sql", "file6.sql", "file7.sql"]
    DBMigrations = ["file1.sql", "file2.sql", "file3.sql", "file4.sql", "file5.sql", "file6.sql", "file7.sql"]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert notUsedMigrations == []

def test_unappliedMigrations_3():
    fMigrations = ["file1.sql", "file2.sql", "file3.sql", "file4.sql", "file5.sql", "file6.sql", "file7.sql", "file8.sql"]
    DBMigrations = ["file1.sql", "file2.sql", "file3.sql", "file4.sql", "file5.sql", "file6.sql"]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert notUsedMigrations == ["file7.sql", "file8.sql"]

def test_actionExecute_1():
    migrationsToUsePrint = "before File and rewrite."
    cursor = fakeCursor()
    paths = [pathlib.Path("file1.sql"), pathlib.Path("file2.sql")]
    actions.actionExecute(cursor, paths)
    assert cursor.outputList[0] == "CREATE TABLE test_sql_archive (login text);" and cursor.outputList[1] == "DROP TABLE test_sql_archive;"

if __name__ == "__main__":
    test_actionExecute_1()