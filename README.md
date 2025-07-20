# Goals
Enhancing reverse engineering capabilites by being able to easily run a script which exports all local types / custom structures defined in IDA to be used in your favorite debugger.

# Usage
```
usage: structbug [-h] [-H HEADER] [-I I64] [-o OUTPUT] [-f FORMAT]

Add support for casting reverse engineered structures in your debugger

options:

  -h, --help            show this help message and exit
  -H HEADER, --header HEADER
                        Provide header file to convert
  -I I64, --i64 I64     Extract types directly from an idb (tilib required in PATH)
  -o OUTPUT, --output OUTPUT
                        Output file name (default: source_name.debug/pdb)
  -f FORMAT, --format FORMAT
                        Debug format DWARF/PDB. (default: current platform)
```

# TODO
- Windows pdb support
- Ghidra support
