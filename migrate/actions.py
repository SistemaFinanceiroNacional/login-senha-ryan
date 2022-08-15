from pathlib import Path
import typing
import psycopg2


def unappliedMigrations(allMigrationsFromArgsFolder: typing.List[Path], allMigrationsApplied: typing.List[Path]) -> typing.List[Path]:
    unappliedMigrationsList: typing.List[Path] = []
    allMigrationsFromArgsFolder.sort()
    for i in allMigrationsFromArgsFolder:
        if i.name[0:8] not in allMigrationsApplied:
            unappliedMigrationsList.append(i)

    return unappliedMigrationsList

def actionExecute(cursor: psycopg2.cursor, migrationsToUse: typing.List[Path]) -> None:
    for i in migrationsToUse:
        with i.open() as file:
            cursor.execute(file.read())

def appliedMigrations(allMigrationsFromArgsFolder, allMigrationsApplied):
    appliedMigrationsList = []
    for i in allMigrationsApplied:
        if i in allMigrationsFromArgsFolder:
            appliedMigrationsList.append(i)