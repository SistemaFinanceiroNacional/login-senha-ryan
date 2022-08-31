#!/usr/bin/python3

import sys
import inputIO
import argparse
import psycopg2
from pathlib import Path
import actions
from collections.abc import Iterable


def main(args, userIO):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", nargs=1, dest="folder", default="migrations")
    parser.add_argument("action", choices=["up", "down"])
    parser.add_argument("-d", "--dbname", nargs=1, default="postgres")
    parser.add_argument("-u", "--user", nargs=1, default="postgres")
    parser.add_argument("--password", nargs=1)
    parser.add_argument("--host", nargs=1, default="localhost")
    parser.add_argument("-p", "--port", nargs=1, default="5432")
    args = parser.parse_args()

    if not args.password:
        args.password = userIO.inputoccult("password:")

    p = Path(f'{args.folder[0]}')
    folderKids = list(p.glob(f'*_{args.action}.sql'))

    with psycopg2.connect(
            f"dbname={args.dbname[0]} user={args.user[0]} password={args.password} host={args.host} port={args.port}") as conn, conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS migrations_applied(id SERIAL PRIMARY KEY, version CHAR(8)")

        if args.action == "up":
            cursor.execute("SELECT version FROM migrations_applied ORDER BY version asc")
            comparablePaths: Iterable[str] = map(lambda x: x[0], cursor.fetchall())

            m = actions.unappliedMigrations(folderKids, comparablePaths)
            actions.actionExecute(cursor, m)

        elif args.action == "down":
            cursor.execute("SELECT version FROM migrations_applied ORDER BY version desc")
            comparableList = cursor.fetchall()


if __name__ == "__main__":
    sys.exit(main(sys.argv, inputIO.inputIO()))
