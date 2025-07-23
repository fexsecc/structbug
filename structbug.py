#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
from struct import pack

def_tmp_name = "3d801aa532c1cec3ee82d87a99fdf63f"

# Change this
vcvarsall_path = r""

def produce_pdb(header, output_name, discard_header=False):
    r"""
    Produce a PDB file containing custom types
    in order to be used within windbg
    """

    if vcvarsall_path:
        vcvars = vcvarsall_path
    else:
        vcvars = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"

    if not os.path.exists(vcvars):
        print("[-] Couldn't find MSVC compiler")
        exit(1)
    else:
        print("[+] Found MSVC compiler")

    # TODO: finish


def run_tilib():
    r"""
    Uses tilib utilitary to parse IDA .til files
    Versions starting with IDA 9.1 come with tilib out of the box
    If missing, install manually
    Then add tilib to PATH
    """

    print("[!] Ensure tilib is on your PATH, located in the $IDA_INSTALL/tools/tilib/ directory")
    res = subprocess.run(
        "tilib -l " + def_tmp_name + ".til",
        shell=True,
        capture_output=True,
        text=True
    )
    
    res.stdout = res.stdout.split('(enumerated by names)')[0]
    idx = res.stdout.split('   8')[1].split('. ')[1:]

    with open(def_tmp_name + ".h", "w") as h:
        for i in range(len(idx)):
            h.write(idx[i].split('\n')[0] + '\n')

    os.system(f"rm -f {def_tmp_name}.til")

def extract_til(idb):
    r"""
    Extract .til local types section from an idb/i64 file
    """

    with open(idb, "rb") as db:
        data = db.read()
        start = data.find(b"IDATIL")
        db.seek(start)
        end = data.find(b"IDAS")
        til_size = end - start
        til = db.read(til_size)
        with open(def_tmp_name + ".til", "wb") as o:
          o.write(til)


def clean_ida_header(header):
    r"""
    Remove default IDA declarations as I cant find __offset
    Anywhere and have no idea what it is
    """

    
    with open(header, "r") as f:
      lines = f.readlines()
    
    exc_start = -1
    exc_end = -1
    for i in range(len(lines)):
      if '/* 1 */\n' == lines[i]:
        exc_start = i
      elif '/* 7 */\n' == lines[i]:
        exc_end = i + 3

    if exc_start == -1 or exc_end == -1:
        return
    
    with open(header, "w") as o:
      for i in range(len(lines)):
        if i < exc_start or i > exc_end:
          o.write(lines[i])


def produce_dwarf(header, output_name, discard_header=False):
    r"""
    Produce a DWARF debug file containing custom types
    in order to be used with gdb/lldb
    """

    with open(def_tmp_name + ".cpp", "w") as src:
        src.write(f'#include "{header}"\n')
    os.system(f"g++ -o {def_tmp_name} {def_tmp_name}.cpp -g3 -c -fno-eliminate-unused-debug-types -fno-eliminate-unused-debug-symbols -O0")
    os.system(f"objcopy --only-keep-debug {def_tmp_name} {output_name}")
    os.system(f"rm -f {def_tmp_name} {def_tmp_name}.cpp")

    if discard_header:
        os.system(f"rm -f {header}")
    print("[+] DWARF file created.")


def main():
    try:
        dbg_formats = {
            "linux"   : "dwarf",
            "darwin"  : "dwarf",
            "android" : "dwarf",
            "win32"   : "pdb"
        }

        parser = argparse.ArgumentParser(
                        prog='structbug',
                        description='Add support for casting reverse engineered structures in your debugger'
        )

        parser.add_argument('-H', "--header", type=str, help="Provide header file to convert")
        parser.add_argument('-I', "--i64", type=str, help="Extract types directly from an idb (tilib required in PATH)")
        parser.add_argument('-o', '--output', type=str, help='Output file name (default: source_name.debug/pdb)')
        parser.add_argument('-f', '--format', type=str, default=dbg_formats.get(sys.platform, 'unk'), help="Debug format DWARF/PDB. (default: current platform)")

        args = parser.parse_args()

        if len(sys.argv) < 2:
            print("No options given. Run -h for a list of options")
            exit(1)

        if not any((args.header, args.i64)):
            print("Source of type information required (ex: header, idb file)")
            exit(1)

        if args.format != 'dwarf' and args.format != 'pdb':
            print("Unknown platform or format, supported platforms:")
            print(dbg_formats.keys())
            exit(1)

        if not args.output:
            if args.header:
                try:
                    args.output = args.header.split('.')[-2] + ('.debug' if args.format == "dwarf" else '.pdb')
                except IndexError:
                    args.output = args.header + ('.debug' if args.format == "dwarf" else '.pdb')
            elif args.i64:
                try:
                    args.output = args.i64.split('.')[-2] + ('.debug' if args.format == "dwarf" else '.pdb')
                except IndexError:
                    args.output = args.i64 + ('.debug' if args.format == "dwarf" else '.pdb')


    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)

    if args.header:
        # In case the header is still taken from IDA,
        # Get rid of unwanted default types
        clean_ida_header(args.header)

        if args.format == 'dwarf':
            produce_dwarf(args.header, args.output)
        elif args.format == 'pdb':
            produce_pdb(args.header, args.output)
    elif args.i64:
        extract_til(args.i64)
        run_tilib()
        if args.format == 'dwarf':
            produce_dwarf(def_tmp_name + ".h", args.output, discard_header=True)
        elif args.format == 'pdb':
            # TODO: Implement pdb creation
            #produce_pdb()
            exit(1)


if __name__ == '__main__':
    main()

