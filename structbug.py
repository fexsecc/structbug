#!/usr/bin/env python3
import argparse
import os

#def run_tilib():
#    # Versions starting with IDA 9.1 come with tilib out of the box
#    # If missing, install it manually
#    # Then add tilib to PATH
#    import subprocess
#
#    proc = subprocess.Popen(["cat", "/etc/passwd"], stdout=subprocess.PIPE, shell=True)
#    (out, err) = proc.communicate()
#    print("program output:", out)
#
#def extract_til():
#    # Extract .til local types section from the idb/i64 file
#    with open(sys.argv[2][:-3] + "til", "rb") as db:
#        data = db.read()
#        start = data.find(b"IDATIL")
#        db.seek(start)
#        end = data.find(b"IDAS")
#        til_size = end - start
#        til = db.read(til_size)
#        with open("./tmp.til", "wb") as o:
#          o.write(til)
#
#
#def clean_ida_header():
#    # Remove default IDA declarations as I cant find __offset
#    # Anywhere and have no idea what it is
#    
#    with open(sys.argv[1], "r") as f:
#      lines = f.readlines()
#    
#    exc_start = -1
#    exc_end = -1
#    for i in range(len(lines)):
#      if '/* 1 */\n' == lines[i]:
#        exc_start = i
#      elif '/* 7 */\n' == lines[i]:
#        exc_end = i + 3
#
#    if exc_start == -1 or exc_end == -1:
#        return
#    
#    with open(sys.argv[1], "w") as o:
#      for i in range(len(lines)):
#        if i < exc_start or i > exc_end:
#          o.write(lines[i])
#
#
#def produce_dwarf():
#    with open("./tmp.cpp", "w") as src:
#        src.write(f'#include "{sys.argv[1]}"\n')
#    os.system("g++ -o tmp tmp.cpp -g3 -c -fno-eliminate-unused-debug-types -fno-eliminate-unused-debug-symbols -O0")
#    os.system(f"objcopy --only-keep-debug tmp {sys.argv[1][:-2]}.debug")
#    os.system("rm -f tmp tmp.c")


def main():
    parser = argparse.ArgumentParser(description="Add support for casting reverse engineered structures in your debugger")
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-H', "--header")
    parser.add_argument('-I', "--i64")
    args = parser.parse_args()

    if not any((args.header, args.i64)):
        print("[X] Please provide a valid type source.")
        exit(2)
    elif args.header and args.i64:
        print("[X] More than one source provided.")
        exit(2)

    #if len(sys.argv) < 2:
    #    print("USAGE: ./structbug.py <header> <optional i64 DB file>")
    #    exit(1)
    #elif len(sys.argv) == 2:
    #    clean_ida_header()
    #    produce_dwarf()
    #elif len(sys.argv) == 3:
    #TODO: Implement argparse mutual exclusive for either --header or --i64
    #    # TODO: implement i64 extraction of db
    #    extract_til()
    #    run_tilib()
    #else:
    #    print("[X] Invalid options given")
    #    print("USAGE: ./structbug.py <header> <optional i64 DB file>")
    #    exit(1)

if __name__ == '__main__':
    main()

