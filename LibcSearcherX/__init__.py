#!/usr/bin/python3
import os
import re
import sys
import json
import requests


class LibcSearcher:
    def __init__(self, symbol_name: str = None, address: int = None, api: str = "https://libc.rip"):
        self.api = api
        self.sym = {}
        self.libc_list = []
        if not isinstance(symbol_name, str):
            print("The function should be a string")
            sys.exit()
        if not isinstance(address, int):
            print("The address should be an int number")
            sys.exit()
        if (symbol_name is not None) and (address is not None):
            self.query(symbol_name, address)
        self.show()

    def query(self, symbol_name, address):
        data = {
            "symbols": {
                symbol_name: hex(address),
            }
        }
        headers = {'Content-Type': 'application/json'}
        self.libc_list = requests.post(url="{}/api/find".format(self.api), headers=headers, data=json.dumps(data)).json()

    def show(self):
        if not self.libc_list:
            print("\x1b[1;31m" + "[+] No libc satisfies constraints." + "\x1b[0m")
            exit(0)
        elif len(self.libc_list) == 1:
            self.dump(self.libc_list[0]["symbols_url"])
        else:
            print("\x1b[33m[+] There are multiple libc that meet current constraints :\x1b[0m")
            self.chose()

    def chose(self, chosen_index: int = -1):
        if chosen_index == -1:
            for index, libc in enumerate(self.libc_list):
                print(str(index) + " - " + libc["id"] + " (" + libc["download_url"] + ")")
            chosen_index = input("\x1b[33m[+] Choose one : \x1b[0m")
        try:
            self.dump(self.libc_list[int(chosen_index)]["symbols_url"])
        except IndexError:
            print("\x1b[1;31m[+] Index out of bound!\x1b[0;m")
            self.chose()

    def dump(self, symbols_url):
        res = requests.get(symbols_url)
        for name_addr in res.text.split("\n")[:-1]:
            name, addr = name_addr.split(" ")
            self.sym[name] = int(addr, 16)


class LibcSearcherLocal(object):
    def __init__(self, symbol_name: str = None, address: int = None, dbpath: str = "libcdb"):
        self.sym = {}
        self.libc_list = []
        if not isinstance(symbol_name, str):
            print("The function should be a string")
            sys.exit()
        if not isinstance(address, int):
            print("The address should be an int number")
            sys.exit()
        if not dbpath.startswith("/"):
            self.libc_database_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), dbpath)
        else:
            self.libc_database_path = dbpath
        if (symbol_name is not None) and (address is not None):
            self.query(symbol_name, address)
        self.show()

    def query(self, symbol_name, address):
        addr_last12 = address & 0xfff
        db = self.libc_database_path
        for _, _, f in os.walk(db):
            for i in f:
                fd = open(os.path.join(db, i), "rb")
                data = fd.read().decode(errors='ignore').split("\n")
                if any(map(lambda line: re.compile("^%s .*%x" % (symbol_name, addr_last12)).match(line), data)):
                    self.libc_list.append(i)

    def show(self):
        if not self.libc_list:
            print("\x1b[1;31m" + "[+] No libc satisfies constraints." + "\x1b[0m")
            exit(0)
        elif len(self.libc_list) == 1:
            self.dump(self.libc_list[0])
        else:
            print("\x1b[33m[+] There are multiple libc that meet current constraints :\x1b[0m")
            self.chose()

    def chose(self, chosen_index: int = -1):
        if chosen_index == -1:
            for index, libc in enumerate(self.libc_list):
                print(str(index) + " - " + libc.rstrip('.symbols'))
            chosen_index = input("\x1b[33m[+] Choose one : \x1b[0m")
        try:
            self.dump(self.libc_list[int(chosen_index)])
        except IndexError:
            print("\x1b[1;31m[+] Index out of bound!\x1b[0;m")
            self.chose()

    def dump(self, symbol_name):
        db = os.path.join(self.libc_database_path, symbol_name)
        fd = open(db, "rb")
        data = fd.read().decode(errors='ignore').strip("\n").split("\n")
        for d in data:
            f = d.split(" ")[0]
            addr = int(d.split(" ")[1], 16)
            self.sym[f] = addr


if __name__ == '__main__':
    libc = LibcSearcher("fgets", 0x7ff39014bd90)
    print("[+]system  offset: ", hex(libc.sym["system"]))
    print("[+]/bin/sh offset: ", hex(libc.sym["str_bin_sh"]))

    libc = LibcSearcherLocal("fgets", 0x7ff39014bd90)
    print("[+]system  offset: ", hex(libc.sym["system"]))
    print("[+]/bin/sh offset: ", hex(libc.sym["str_bin_sh"]))
