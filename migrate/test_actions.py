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
    paths = [pathlib.Path("/home/ryan/Documents/login-senha-ryan/migrate/file1.sql"), pathlib.Path("/home/ryan/Documents/login-senha-ryan/migrate/file2.sql")]
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
    DBMigrations = ["20220708"]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert notUsedMigrations == []

def test_downMigrations_2_migrations():
    appliedMigrationVersion = "20230101"
    fMigrations = [pathlib.Path("20220709_create_service_table_up.sql"), pathlib.Path("20220709_outdate_service_table_down.sql"),
                   pathlib.Path("20221008_update_account_table_up.sql"), pathlib.Path("20221008_outdate_account_table_down.sql")]
    downMigrations = actions.downMigrations(fMigrations, appliedMigrationVersion)
    assert downMigrations == [pathlib.Path("20221008_outdate_account_table_down.sql"), pathlib.Path("20220709_outdate_service_table_down.sql")]

def test_downMigrations_0_migrations():
    appliedMigrationVersion = "20230101"
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"), pathlib.Path("20220709_create_service_table_up.sql")]
    downMigrations = actions.downMigrations(fMigrations, appliedMigrationVersion)
    assert downMigrations == []

def test_downMigrations_1_migration():
    appliedMigrationsVersion = "20220809"
    fMigrations = [pathlib.Path("20220709_create_service_table_up.sql"), pathlib.Path("20220709_outdate_service_table_down.sql"),
                   pathlib.Path("20220801_update_account_table_up.sql"), pathlib.Path("20220801_outdate_account_table_down.sql"),
                   pathlib.Path("20220807_insert_ryan_account_into_accounts_table_up.sql"), pathlib.Path("20220807_delete_ryan_account_from_accounts_table_down.sql"),
                   pathlib.Path("20220809_update_ryan_balance_into_accounts_table_up.sql"), pathlib.Path("20220809_decrease_ryan_balance_from_account_table_down.sql"),
                   pathlib.Path("20221008_insert_pedro_account_into_accounts_table_up.sql"), pathlib.Path("20221008_delete_pedro_account_from_accounts_table_down.sql")]
    downMigrations = actions.downMigrations(fMigrations, appliedMigrationsVersion)
    assert downMigrations == [pathlib.Path("20220809_decrease_ryan_balance_from_account_table_down.sql"),
                              pathlib.Path("20220807_delete_ryan_account_from_accounts_table_down.sql"),
                              pathlib.Path("20220801_outdate_account_table_down.sql"),
                              pathlib.Path("20220709_outdate_service_table_down.sql")]


def test_down_migrations_using_migrations_folder():
    lastMigrationApplied = "20221101"
    p = pathlib.Path('../migrations')
    folderKids = sorted(p.glob('*.sql'))
    downMigrations = actions.downMigrations(folderKids, lastMigrationApplied)
    assert downMigrations == [pathlib.Path("../migrations/20221101_insert_into_accounts_ryan_accounts_down.sql"),
                              pathlib.Path("../migrations/20221030_delete_from_accounts_joao_account_down.sql"),
                              pathlib.Path("../migrations/20220704_drop_account_table_down.sql")]


def test_version_unappliedMigrations():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"),pathlib.Path("20220810_update_account_tablee_up.sql"),pathlib.Path("20220920_update_account_table_up.sql"), pathlib.Path("20221008_update_account_table_up.sql")]
    DBMigrations = ["20220708"]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert len(notUsedMigrations) == len(fMigrations) - 1

def test_version_unappliedMigrations1():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"),pathlib.Path("20220810_update_account_tablee_up.sql"),pathlib.Path("20220920_update_account_table_up.sql"), pathlib.Path("20221008_update_account_table_up.sql")]
    DBMigrations = ["20221008"]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert len(notUsedMigrations) == 0

def test_version_unappliedMigrations_empty_list():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"),pathlib.Path("20220810_update_account_tablee_up.sql"), pathlib.Path("20220920_update_account_table_up.sql"), pathlib.Path("20221008_update_account_table_up.sql")]
    DBMigrations = []
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert len(notUsedMigrations) == 4

def test_version_unappliedMigrations_emptyString_on_list():
    fMigrations = [pathlib.Path("20220708_update_account_table_up.sql"),pathlib.Path("20220810_update_account_tablee_up.sql"), pathlib.Path("20220920_update_account_table_up.sql"), pathlib.Path("20221008_update_account_table_up.sql")]
    DBMigrations = [""]
    notUsedMigrations = actions.unappliedMigrations(fMigrations, DBMigrations)
    assert len(notUsedMigrations) == 4


if __name__ == "__main__":
    test_down_migrations_using_migrations_folder()