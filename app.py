#!/bin/python3
import os
import sqlite3
import sys
import readline
import textwrap

VERSION = "09/07, 2023"
conn, dbpath = None, None

SEEK = None
TB = None

def info() -> None:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")
    li = []
    for i in cur:
        n = i[0]
        if n == 'sqlite_sequence':
            continue
        li.append(n)
    for i in li:
        print(i, end='  ')
    if len(li) != 0:
        print()
    global TB
    TB = li
    cur.close()

"""
SELECT * FROM `2023` WHERE month=9 AND day=5;
"""
def select(args) -> str:
    global SEEK
    SEEK = args[0]

    if len(args) == 1:
        sum = 0
        for i in range(1, 13):
            cur = conn.execute(
                "SELECT COUNT() FROM `{}` WHERE month={}"
                .format(args[0], i)
            )
            num = cur.fetchone()[0]
            sum += num

            print("{:<2}({})\t".format(i, num), end='')
            if i % 4 == 0:
                print()
            cur.close()
        print("sum %d" % sum)
    elif len(args) == 2:
        cur = conn.execute(
            "SELECT id, day, title FROM `{}` WHERE month={} ORDER BY day"
            .format(args[0], args[1])
        )
        li = cur.fetchall()

        if len(li) == 0:
            print("empty")
        else:
            for i in li:
                print("id={:>3} {:>4} \"{}\"".format(i[0], i[1], i[2]))
        cur.close()

def inspect() -> bool:
    if SEEK == None:
        print("require '.select' to select a table")
        return True

"""
INSERT INTO `2023`(
    month, day, title, content) VALUES(
        9, 5, 'this is title', 'qwer');
"""
def insert(arg):
    if inspect():
        return
    if len(arg) != 2:
        print("need month and day to set")
        return
    month = arg[0]
    day = arg[1]

    try:
        title = input("title: ")
        content = input("content: ")

        d = (month, day, title, content)
        cur = conn.execute(
            "INSERT INTO `{}`(month, day, title, content) VALUES(?, ?, ?, ?)"
            .format(SEEK), d
        )
        print("OK, id=%d" % cur.lastrowid)
        cur.close()
    except KeyboardInterrupt:
        print("\nbreak")
        return

def show(id):
    if inspect():
        return
    cur = conn.execute("SELECT * FROM `{}` WHERE id={}".format(SEEK, id[0]))
    li = cur.fetchall()

    if len(li) == 0:
        print("empty")
    else:
        for i in li:
            t = textwrap.fill(i[4], width=20)
            print(
                "id={} ({:0>2d}/{:0>2d}, \"{}\")\n"
                .format(i[0], i[1], i[2], SEEK)
            )
            print("{}\n\n{}".format(i[3], t))

def delete(id):
    if inspect():
        return
    i = int(id[0])
    p = input("record with id %d? Enter/N " % i)

    if len(p) == 0:
        cur = conn.execute(
            "DELETE FROM `{}` WHERE id={}"
            .format(SEEK, i)
        )
        print("OK")
        cur.close()
    else:
        print("abort")

def new(name):
    p = conn.execute("""
CREATE TABLE `%s`(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TINYINT(1) NOT NULL,
    day TINYINT(1) NOT NULL,
    title VARCHAR(128) NOT NULL,
    content VARCHAR(255) NOT NULL
);
""" % name[0])
    print("OK")
    p.close()

def drop(name):
    if name[0] == "*":
        if TB == None:
            print("require '.info' to pull tables")
            return
        if len(TB) == 0:
            print("table list is empty")
            return
        p = input("drop all tables?\n  %s\nEnter/N " % "  ".join(TB))
        if len(p) == 0:
            for i in TB:
                cur = conn.execute("DROP TABLE `%s`" % i)
                cur.close()
            print("OK")
        else:
            print("abort")
    else:
        p = input("drop table %s? Enter/N " % name[0])
        if len(p) == 0:
            cur = conn.execute("DROP TABLE `%s`" % name[0])
            cur.close()
            print("OK")
        else:
            print("abort")

def clear():
    cur = conn.execute("VACUUM")
    print("OK %dkb" % (os.path.getsize(dbpath) / 1000))
    cur.close()

ENTRY = {".select": select, ".show"  : show,
         ".delete": delete, ".new"   : new,
         ".drop"  : drop,   ".insert": insert}

def eval(com):
    match com:
        case ".help":
            print(""".info           print saved principal information
.new NAME       create a new table
.drop *,NAME    drop one or more tables
.select NAME,M  simply select table and month
.show ID        print entry
.delete ID      delete entry
.insert M,D     go to innsert command prompt
.clear          execute the sqlite3 vacuum command
.quit           just exit""")
        case ".info":
            info()
        case ".clear":
            clear()
        case _:
            p = com.split()
            command = p[0]

            if len(p) == 1:
                for i in ENTRY:
                    if i == command:
                        print("need to carry parameters")
                        return
            del p[0]
            try:
                ENTRY[command](p)
            except KeyError:
                print("undefined")

def main():
    args = sys.argv

    if len(args) == 1:
        print("usage: app.py *.db")
        return
    global conn, dbpath
    conn = sqlite3.connect(args[1], isolation_level=None)
    dbpath = args[1]

    print("""Version: {}
Connected: '{}'
Type '.help' to print help information
     '.quit' to exit program""".format(VERSION, args[1]))
    while True:
        try:
            com = input("> ")
            if com == ".quit":
                conn.close()
                break
            if com == "" or len(com.rstrip()) == 0:
                continue
            eval(com)
        except KeyboardInterrupt:
            conn.close()
            print("\ndatabase closed, exit.")
            break
        except Exception as e:
            print(e.__str__())

main()