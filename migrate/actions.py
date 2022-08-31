import pathlib
from pathlib import Path
import typing
from collections.abc import Iterable
from genericCursor import genericCursor

def unappliedMigrations(allMigrationsFromArgsFolder: typing.List[Path], allMigrationsApplied: typing.List[str]) -> typing.List[Path]:
    unappliedMigrationsList: typing.List[Path] = []
    for i in allMigrationsFromArgsFolder:
        version = i.name.split("_")
        if version[0] not in allMigrationsApplied:
            unappliedMigrationsList.append(i)

    return unappliedMigrationsList

def actionExecute(cursor: genericCursor, migrationsToUse: typing.List[Path]) -> None:
    for i in migrationsToUse:
        with i.open() as file:
            cursor.execute(file.read())

def appliedMigrations(allMigrationsFromArgsFolder, allMigrationsApplied):
    appliedMigrationsList = []
    for i in allMigrationsApplied:
        if i in allMigrationsFromArgsFolder:
            appliedMigrationsList.append(i)
    return appliedMigrationsList