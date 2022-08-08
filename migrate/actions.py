

def unappliedMigrations(allMigrationsFromArgsFolder, allMigrationsApplied):
    unappliedMigrationsList = []
    allMigrationsFromArgsFolder.sort()
    for i in allMigrationsFromArgsFolder:
        if i.name[0:8] not in allMigrationsApplied:
            unappliedMigrationsList.append(i)

    return unappliedMigrationsList

def actionExecute(cursor, migrationsToUse):
    for i in migrationsToUse:
        with i.open() as file:
            cursor.execute(file.read())

def appliedMigrations(allMigrationsFromArgsFolder, allMigrationsApplied):
    appliedMigrationsList = []
    for i in allMigrationsApplied:
        if i in allMigrationsFromArgsFolder:
            appliedMigrationsList.append(i)