# LibcSearcherX

LibcSearcher for python3

## Build
```bash
python3 setup.py sdist
pip3 install LibcSearcherX-0.0.3.tar.gz
```


## Usage
```python
from LibcSearcherX import LibcSearcher, LibcSearcherLocal

libc = LibcSearcher("fgets", 0x7ff39014bd90)
print("[+]system  offset: ", hex(libc.sym["system"]))
print("[+]/bin/sh offset: ", hex(libc.sym["str_bin_sh"]))

libc = LibcSearcherLocal("fgets", 0x7ff39014bd90)
print("[+]system  offset: ", hex(libc.sym["system"]))
print("[+]/bin/sh offset: ", hex(libc.sym["str_bin_sh"]))
```
