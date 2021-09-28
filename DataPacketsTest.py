import unittest

from DataPacket_lib import *


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


test_fields = [Field(string_name='Test 16 bit', attribute_name='full_word', meaning=0, bit_length=16),
               Field(string_name='Test 8_1 bit', attribute_name='half_word_1', meaning=0, bit_length=8),
               Field(string_name='Test 8_2 bit', attribute_name='half_word_2', meaning=0, bit_length=8),
               Field(string_name='Test 9 bit', attribute_name='bit9', meaning=0, bit_length=9),
               Field(string_name='Test 5 bit', attribute_name='bit5', meaning=0, bit_length=5),
               Field(string_name='Test 1 bit', attribute_name='bit1', meaning=0, bit_length=1),
               Field(string_name='Test 15 bit', attribute_name='bit15', meaning=0, bit_length=15)]

test_bytes = (1234567891011121314).to_bytes(8, 'big')


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_block = Block.create_from_fields(test_fields)
        self.filled_test_block = self.test_block.copy()
        self.filled_test_block.fill_with_bytes(test_bytes)
        # self.test_block = PacketTest()

    def test_fill_with_bytes(self):
        self.test_block.fill_with_bytes(test_bytes)
        self.assertEqual(test_bytes, self.test_block.bytes_view())

    def test_get_attr(self):
        attr_names = [field.attribute_name for field in test_fields]
        result = [hasattr(self.filled_test_block, attr_name) for attr_name in attr_names]
        self.assertTrue(all(result))


if __name__ == '__main__':
    unittest.main()
