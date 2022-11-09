import pathlib
from pathlib import Path
import typing
from collections.abc import Iterable
from genericCursor import genericCursor


def unappliedMigrations(allMigrationsFromArgsFolder: typing.List[Path], allMigrationsApplied: typing.List[str]) -> typing.List[Path]:
    if len(allMigrationsApplied) == 0:
        return allMigrationsFromArgsFolder

    unappliedMigrationsList: typing.List[Path] = []
    lastMigrationApplied = allMigrationsApplied[0]
    for i in allMigrationsFromArgsFolder:
        version = i.name.split("_")
        if version[0] > lastMigrationApplied:
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

def downMigrations(allMigrationsFromArgsFolder: typing.List[Path], versionOfLastMigrationApplied: str) -> typing.List[Path]:
    downMigrationsList = []
    for migration in allMigrationsFromArgsFolder:
        migrationData = migration.name.split("_")
        action = migrationData[-1].split(".")[0]
        if migrationData[0] <= versionOfLastMigrationApplied and action == "down":
            downMigrationsList.append(migration)

    downMigrationsList.reverse()

    return downMigrationsList
