from pathlib import Path
import typing
import psycopg2
from collections import Iterable

def unappliedMigrations(allMigrationsFromArgsFolder: Iterable[Path], allMigrationsApplied: Iterable[Path]) -> typing.List[Path]:
    unappliedMigrationsList: typing.List[Path] = []
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