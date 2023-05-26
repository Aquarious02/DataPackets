import unittest

from data_packets.packets import *


class PacketTest(Block):
    _fields_ = [
        ('full_word', c_uint16, 16),
        ('half_word_1', c_uint16, 8),
        ('half_word_2', c_uint16, 8),
        ('bit9', c_uint16, 9),
        ('bit5', c_uint16, 5),
        ('bit1', c_uint16, 1),
        ('bit15', c_uint16, 15),
    ]

    _field_names_ = [
        ('full_word', 'Test 16 bit'),
        ('half_word_1', 'Test 8_1 bit'),
        ('half_word_2', 'Test 8_2 bit'),
        ('bit9', 'Test 9 bit'),
        ('bit5', 'Test 5 bit'),
        ('bit1', 'Test 1 bit'),
        ('bit15', 'Test 15 bit'),
    ]


test_fields = [
    Field(item_name='Test 16 bit', attribute_name='full_word', meaning=0, bit_length=16),
    Field(item_name='Test 8_1 bit', attribute_name='half_word_1', meaning=0, bit_length=8),
    Field(item_name='Test 8_2 bit', attribute_name='half_word_2', meaning=0, bit_length=8),
    Field(item_name='Test 9 bit', attribute_name='bit9', meaning=0, bit_length=9),
    Field(item_name='Test 7 bit', attribute_name='bit7', meaning=0, bit_length=7),
    Field(item_name='Test 1 bit', attribute_name='bit1', meaning=0, bit_length=1),
    Field(item_name='Test 15 bit', attribute_name='bit15', meaning=0, bit_length=15)
]

test_bytes = (1234567891011121314).to_bytes(8, 'big')


class TestBlock(unittest.TestCase):
    def setUp(self) -> None:
        self.test_block = Block.create_from_fields(test_fields)
        self.filled_test_block = self.test_block.copy()
        self.filled_test_block.fill_with_bytes(test_bytes)
        # self.test_block = PacketTest()

    def test_fill_with_bytes(self):
        self.test_block.fill_with_bytes(test_bytes)
        with self.subTest('Compare to test bytes'):
            self.assertEqual(test_bytes, self.test_block.bytes_view())

        with self.subTest('Compare bytes() and bytes_view()'):
            # self.assertEqual(self.test_block.bytes_view(), self.filled_test_block.bytes_view())
            self.assertEqual(bytes(self.filled_test_block), self.filled_test_block.bytes_view())

        with self.subTest('Compare with copy'):
            self.assertEqual(self.test_block.bytes_view(), self.filled_test_block.bytes_view())

        with self.subTest('Compare test bytes and value in filled_test_block'):
            self.assertEqual(self.filled_test_block.half_word_1, test_bytes[2])

    def test_get_attr(self):
        result = [hasattr(self.filled_test_block, attr_name) for attr_name in map(lambda x: x.attribute_name, test_fields)]
        self.assertTrue(all(result))


class TestPacket(unittest.TestCase):
    def setUp(self) -> None:
        self.test_packet = Packet(children_blocks=[Block.create_from_fields(test_fields[:3]), Block.create_from_fields(test_fields[3:])])
        self.test_packet.fill_with_bytes(test_bytes)

    def test_bytes_view(self):
        self.assertEqual(test_bytes.hex(' ', 2), self.test_packet.bytes_view().hex(' ', 2))

    def test_get_item(self):
        item_name = test_fields[-1].item_name
        self.assertNotEqual(None, self.test_packet[item_name])


if __name__ == '__main__':
    unittest.main()
