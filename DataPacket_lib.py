import ctypes

# Types aliases (now import from BinaryStream)
c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16
c_uint32 = ctypes.c_uint32
c_int32 = ctypes.c_int32
c_float = ctypes.c_float
c_bool = ctypes.c_bool


class Field:
    """
    Field of one parameter
    """
    def __init__(self, string_name, attribute_name, meaning=None, c_type=c_uint16, bit_length=16, check_range=None):
        """
        :param string_name: name to show in print
        :param meaning: value of field
        :param bit_length: length in bits of value in bytestream
        :param check_range: valid range of values
        """
        self.string_name = string_name
        self.attribute_name = attribute_name
        self.meaning = meaning
        self.c_type = c_type
        self.length = bit_length
        self.check_range = check_range

    # def __bytes__(self):
    #     return


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
            _fields.append((field.attribute_name, field.c_type, field.length))
            _field_names.append((field.attribute_name, field.string_name))

        FutureClass = type("DataPacket", (cls,), {'_fields_': _fields, '_field_names_': _field_names, 'fields': fields})
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
        pass

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
        new_object = self.create_from_fields(self.fields)
        new_object.__dict__ = self.__dict__.copy()
        return new_object


class Block(ctypes.LittleEndianStructure, BlockBase):
    pass


class PacketTest(Block):
    _fields_ = [('full_word', c_uint16, 16),
                ('half_word_1', c_uint16, 8),
                ('half_word_2', c_uint16, 8),
                ('bit9', c_uint16, 9),
                ('bit5', c_uint16, 5),
                ('bit1', c_uint16, 1),
                ('bit15', c_uint16, 15)]

    _field_names_ = [('full_word', 'Test 16 bit'),
                     ('half_word_1', 'Test 8_1 bit'),
                     ('half_word_2', 'Test 8_2 bit'),
                     ('bit9', 'Test 9 bit'),
                     ('bit5', 'Test 5 bit'),
                     ('bit1', 'Test 1 bit'),
                     ('bit15', 'Test 15 bit')]


class Packet(Block):
    """
    Packet consists of blocks, has limited len
    """
    pass
