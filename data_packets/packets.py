import ctypes

# Types aliases (now import from BinaryStream)
from _ctypes import _SimpleCData
from dataclasses import dataclass

c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16
c_uint32 = ctypes.c_uint32
c_int32 = ctypes.c_int32
c_float = ctypes.c_float
c_bool = ctypes.c_bool


@dataclass
class Field:
    """
    Field of one parameter
    """
    item_name: str
    """Name to show in print"""
    attribute_name: str
    meaning: int | float | bytes = None
    """Value of field"""
    c_type: _SimpleCData = c_uint16
    bit_length: int = 16
    """Length in bits of value in bytestream"""


class BlockBase:
    _pack_ = 1
    _fields_ = []
    _field_names_ = []
    """
    BlockBase consists of fields
    """
    def __init__(self):
        super(BlockBase, self).__init__()
        self.bytes_buffer = b''
        self.fields = []

    @classmethod
    def create_from_fields(cls, fields):
        _fields, _field_names = [], []
        for field in fields:
            _fields.append((field.attribute_name, field.c_type, field.bit_length))
            _field_names.append((field.attribute_name, field.item_name))

        FutureClass = type("DataPacket", (cls,), {'_fields_': _fields, '_field_names_': _field_names,
                                                  '_pack_': 1, 'fields': fields})
        return FutureClass()

    def clear(self):
        self._fields_.clear()
        self._field_names_.clear()

    def fill_with_fields(self, fields):
        for field in fields:
            self._fields_.append((field.attribute_name, field.c_type, field.length))
            self._field_names_.append((field.attribute_name, field.string_name))
            setattr(self, field.attribute_name, field.meaning or 0)

    @classmethod
    def create_from_bytes(cls, _bytes):
        instance = cls()
        instance.fill_with_bytes(_bytes)
        return instance

    def fill_with_bytes(self, _bytes):
        if self._fields_:
            _bytes_len = min(len(_bytes), ctypes.sizeof(self))
            # _bytes_len = max(len(_bytes), ctypes.sizeof(self))
            buffer = ctypes.create_string_buffer(bytes(_bytes), len(_bytes))
            ctypes.memmove(ctypes.addressof(self), buffer, _bytes_len)
        else:
            self.bytes_buffer = _bytes

    def bytes_view(self):
        if self._fields_:
            return bytes(self)
        else:
            return self.bytes_buffer

    def copy(self):
        new_object = type("DataPacket", (type(self),), self.__dict__.copy())
        return new_object()

    def __getitem__(self, item_name):
        for attr_name, field_name in self._field_names_:
            if item_name == field_name:
                return getattr(self, attr_name)

    def __setitem__(self, key, value):
        # for attr_name, field_name in self._field_names_:
        pass

    def __len__(self):
        return ctypes.sizeof(self)


class Block(ctypes.LittleEndianStructure, BlockBase):
    pass


class Packet:
    """
    Packet consists of blocks, has limited len
    """
    def __init__(self, children_blocks=None):
        self.children_blocks = children_blocks or []

    def fill_with_bytes(self, _bytes):
        start = 0
        for block in self.children_blocks:
            stop = len(block)
            block.fill_with_bytes(_bytes[start: start + stop])
            start = stop

    def bytes_view(self):
        all_bytes = b''
        for block in self.children_blocks:
            all_bytes += block.bytes_view()
        return all_bytes

    def __getitem__(self, item_name):
        for block in self.children_blocks:
            if item := block.__getitem__(item_name):
                return item

    def __bytes__(self):
        return self.bytes_view()
