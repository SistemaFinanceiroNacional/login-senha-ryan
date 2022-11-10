#!/usr/bin/python3

import sys
sys.path.append("../inputIO")
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
    parser.add_argument("--host", nargs=1, default=["localhost"])
    parser.add_argument("-p", "--port", nargs=1, default="5432")
    args = parser.parse_args()

    if not args.password:
        args.password = userIO.inputoccult("password:")

    p = Path(f'../{args.folder}')
    folderKids = sorted(p.glob(f'*_{args.action}.sql'))

    with psycopg2.connect(
            f"dbname={args.dbname[0]} user={args.user[0]} password={args.password[0]} host={args.host[0]} port={args.port}") as conn, conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS migrations_applied(version CHAR(8));")

        if args.action == "up":
            cursor.execute("SELECT version FROM migrations_applied")
            version = cursor.fetchall()
            comparablePaths: Iterable[str] = map(lambda i: i[0], version)
            m = actions.unappliedMigrations(folderKids, list(comparablePaths))
            if len(m) > 0:
                actions.actionExecute(cursor, m)
                recentMigrations = m[-1].name.split("_")[0]
                if len(m) == len(folderKids):
                    cursor.execute(f"INSERT INTO migrations_applied(version) VALUES ({recentMigrations});")

                else:
                    cursor.execute(f"UPDATE migrations_applied SET version = {recentMigrations}")

        elif args.action == "down":
            cursor.execute("SELECT version FROM migrations_applied")
            version = cursor.fetchone()
            if version is not None:
                version = version[0]
                downMigrations = actions.downMigrations(folderKids, version)
                if len(downMigrations) > 0:
                    actions.actionExecute(cursor, downMigrations)
                    cursor.execute("DELETE FROM migrations_applied")

            else:
                print("There is no migration applied.")


if __name__ == "__main__":
    sys.exit(main(sys.argv, inputIO))
