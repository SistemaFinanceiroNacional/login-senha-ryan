#!/usr/bin/python3

import sys
import inputIO
import argparse
import psycopg2

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

    with psycopg2.connect(f"dbname={args.dbname[0]} user={args.user[0]} password={args.password} host={args.host} port={args.port}") as conn, conn.cursor() as cursor:
        cursor.execute("CREATE TABLE atesttable (login text, password text, balance int)")
        cursor.execute("INSERT INTO atesttable VALUES (%s, %s, %s)", ("loginTest", "passwordTest", 100))
        cursor.execute("SELECT * FROM atesttable")
        print(cursor.fetchone())


if __name__ == "__main__":
    sys.exit(main(sys.argv, inputIO.inputIO()))
