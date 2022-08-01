

def unappliedMigrations(allMigrationsFromArgsFolder, allMigrationsApplied):
    unappliedMigrationsList = []
    for i in allMigrationsFromArgsFolder:
        if i not in allMigrationsApplied:
            unappliedMigrationsList.append(i)

    return unappliedMigrationsList

def actionExecute(cursor, migrationsToUse):
    for i in migrationsToUse:
        with i.open() as file:
            cursor.execute(file.read())