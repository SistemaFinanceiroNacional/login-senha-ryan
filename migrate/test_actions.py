import actions
import pathlib

class fakeCursor:
    def __init__(self):
        self.outputList = []

    def execute(self, string: str) -> None:
        self.outputList.append(string)

def test_actionExecute_1():
    migrationsToUsePrint = "before File and rewrite."
    cursor = fakeCursor()
    paths = [pathlib.Path("file1.sql"), pathlib.Path("file2.sql")]
    actions.actionExecute(cursor, paths)
    assert cursor.outputList[0] == "CREATE TABLE test_sql_archive (login text);" and cursor.outputList[1] == "DROP TABLE test_sql_archive;"


def test_appliedMigrations_1():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220612_insert_values_into_account_table_up.sql"), pathlib.Path("20220512_create_account_table_up.sql")]
    DBMigrations = [pathlib.Path("20220512_create_account_table_up.sql"), pathlib.Path("20220708_update_account_table_up.sql")]
    applied = actions.appliedMigrations(fMigrations, DBMigrations)
    assert applied == [pathlib.Path("20220512_create_account_table_up.sql"), pathlib.Path("20220708_update_account_table_up.sql")]

def test_appliedMigrations_2():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220612_insert_values_into_account_table_up.sql")]
    DBMigrations = [pathlib.Path("20220512_create_account_table_up.sql"), pathlib.Path("20220708_update_account_table_up.sql")]
    applied = actions.appliedMigrations(fMigrations, DBMigrations)
    assert applied == [pathlib.Path("20220708_update_account_table_up.sql")]

def test_unappliedMigrations_4():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql")]
    DBMigrations = ["20220708_update_account_table_up.sql"]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert notUsedMigrations[0] == pathlib.Path("20220708_update_account_table_up.sql")

def test_downMigrations_1():
    appliedMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220709_create_service_table_up.sql")]
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220709_create_service_table_up.sql"), pathlib.Path("20220709_drop_service_table_down.sql"), pathlib.Path("20220708_outdated_account_table_down.sql")]
    downMigrations = actions.downMigrations(fMigrations, appliedMigrations)
    assert downMigrations == [pathlib.Path("20220708_outdated_account_table_down.sql"), pathlib.Path("20220709_drop_service_table_down.sql")]

def test_downMigrations_2():
    appliedMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220709_create_service_table_up.sql")]
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220709_create_service_table_up.sql"), pathlib.Path("20220709_drop_service_table_down.sql")]
    downMigrations = actions.downMigrations(fMigrations, appliedMigrations)
    assert downMigrations == [ pathlib.Path("20220709_drop_service_table_down.sql")]


if __name__ == "__main__":
    test_actionExecute_1()