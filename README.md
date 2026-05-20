# Goals
Enhancing reverse engineering capabilites by being able to easily run a script which exports all local types / custom structures defined in IDA to be used in your favorite debugger.

# Usage
## Platform Notes: gcc is used by default on linux, and **clang** on Windows. At the time of writing I could not find fitting compiler options for MSVC
### Headers
Easiest way to get started is by creating a header file with your definitions:
```c
typedef struct {
  double volume;
  char* label;
} cylinder;
```
Then run structbug like so:
```bash
structbug.py -H custom_structs.h
```
### DWARF
If all goes well, a .debug file will appear in cwd. To load it into gdb run `add-symbol-file custom_structs.debug`:
```
pwndbg> add-symbol-file ./custom_structs.debug
add symbol table from file "./custom_structs.debug"
Reading symbols from ./custom_structs.debug...
pwndbg> dt cylinder
cylinder
    +0x0000 volume               : double
    +0x0008 label                : char *

```
### PDB
If all goes well, a .pdb file will appear in cwd. To load it into windbg, assuming file is FakeTypes.pdb and in kernel mode:
```
// Store the .pdb with the name without .sys in Symbols/
.sympath+ C:\Symbols\
// Use .exe instead of .sys for user mode
.reload /i /f FakeTypes.sys=0x10000000,0x10000
```

### Ida database
Provided tilib is in your path, or you provide its full path using the `-t` argument, you can do:
```bash
structbug.py -I mystery_program.i64
```

## Using different compilers
### DWARF
```bash
# Example to compile using the arm-linux-gnueabihf toolchain
structbug.py ... -c arm-linux-gnueabihf-
```
### PDB
```powershell
# Specifying a custom compiler is possible although not very useful currently
structbug.py ... -c C:\Tooling\LLVM_20.1.0\bin\clang++
```

# TODO
- Ghidra support (soon™)
