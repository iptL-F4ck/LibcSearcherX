#!/usr/bin/python3
import json
import requests


class LibcSearcher:
    def __init__(self, symbol_name: str = None, address: int = None, api: str = "https://libc.rip"):
        self.api = api
        self.sym = {}
        self.libc_list = []
        if (symbol_name is not None) and (address is not None):
            self.query(symbol_name, address)
        self.show()

    def query(self, symbol_name, address):
        data = {
            "symbols": {
                symbol_name: address,
            }
        }
        headers = {'Content-Type': 'application/json'}
        self.libc_list = requests.post(url=f"{self.api}/api/find", headers=headers, data=json.dumps(data)).json()

    def show(self):
        if not self.libc_list:
            print("\x1b[1;31m" + "[+] No libc satisfies constraints." + "\x1b[0m")
            exit(0)
        elif len(self.libc_list) == 1:
            self.dump(self.self.libc_list[0]["symbols_url"])
        else:
            print("\x1b[33m[+] There are multiple libc that meet current constraints :\x1b[0m")
            self.chose()

    def chose(self, chosen_index: int = -1):
        if chosen_index == -1:
            for index, libc in enumerate(self.libc_list):
                print(str(index) + " - " + libc["id"])
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


if __name__ == '__main__':
    libc = LibcSearcher("strncpy", "db0")
    system_addr = libc.sym['system']
    print(hex(system_addr))
