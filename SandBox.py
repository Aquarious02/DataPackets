import ctypes

from DataPacket_lib import *


if __name__ == '__main__':
    pass
    a = c_uint16(10)
    print(ctypes.byref(a))