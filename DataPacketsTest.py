import unittest

from DataPacket_lib import *

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
        # self.test_block = PacketTest()

    def test_fill_with_bytes(self):
        self.test_block.fill_with_bytes(test_bytes)
        self.assertEqual(test_bytes, self.test_block.bytes_view())
        pass


if __name__ == '__main__':
    unittest.main()
