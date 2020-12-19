from ctypes import cdll

shared_lib = cdll.LoadLibrary('./lib_py_b.so')

class Bonk:

    def __init__(self):
        self.obj = shared_lib.Bonk_new()

    def add(self,a,b):
        return shared_lib.Bonk_add(self.obj,a,b)

def main():
    b = Bonk()
    print(b.add(2,3))

if __name__ == '__main__':
    main()