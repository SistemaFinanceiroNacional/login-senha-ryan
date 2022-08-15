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


def test_appliedMigrations_1():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220612_insert_values_into_account_table_up.sql"), pathlib.Path("20220512_create_account_table_up.sql")]
    DBMigrations = [pathlib.Path("20220512_create_account_table_up.sql"), pathlib.Path("20220708_update_account_table_up.sql")]
    downMigrations = actions.appliedMigrations(fMigrations,DBMigrations)
    assert downMigrations == [pathlib.Path("20220512_drop_account_table_down.sql"), pathlib.Path("20220708_do_not_update_account_table_down.sql")]

def test_unappliedMigrations_4():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql")]
    DBMigrations = [pathlib.Path("20220708_update_account_table_up.sql")]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert notUsedMigrations == pathlib.Path("20220708")



if __name__ == "__main__":
    test_actionExecute_1()