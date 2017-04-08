#!/usr/bin/env python
import unittest

from vpc_subnet_calculator import *


class TestGetNextBinary(unittest.TestCase):
    def test_non_binary_integers(self):
        self.assertEqual(get_next_binary(3), 4)
        self.assertEqual(get_next_binary(5), 8)
        self.assertEqual(get_next_binary(9), 16)

    def test_binary_integers(self):
        self.assertEqual(get_next_binary(2), 4)
        self.assertEqual(get_next_binary(4), 8)
        self.assertEqual(get_next_binary(8), 16)

class TestCalculateSubnets(unittest.TestCase):
    def test_calculate_public_subnets(self):
        self.assertEqual(
            calculate_public_subnets('192.168.0.0/16', 2),
            ['192.168.0.0/18',
            '192.168.64.0/18']
        )
        self.assertEqual(
            calculate_public_subnets('192.168.0.0/16', 3),
            ['192.168.0.0/18',
            '192.168.64.0/18',
            '192.168.128.0/18']
        )
        self.assertEqual(
            calculate_public_subnets('192.168.0.0/16', 5),
            ['192.168.0.0/19',
            '192.168.32.0/19',
            '192.168.64.0/19',
            '192.168.96.0/19',
            '192.168.128.0/19']
        )

if __name__ == '__main__':
    unittest.main()
