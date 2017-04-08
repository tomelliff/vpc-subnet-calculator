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

class TestSubtractSubnetsFromRange(unittest.TestCase):
    def test_subtract_subnets_from_range(self):
        self.assertEqual(
            subtract_subnets_from_range(
                '192.168.0.0/16',
                ['192.168.0.0/18',
                '192.168.64.0/18']),
            '192.168.128.0/17'
        )
        self.assertEqual(
            subtract_subnets_from_range(
                '192.168.0.0/16',
                ['192.168.0.0/18',
                '192.168.64.0/18',
                '192.168.128.0/18']),
            '192.168.192.0/18'
        )
        self.assertEqual(
            subtract_subnets_from_range(
                '192.168.0.0/16',
                ['192.168.0.0/19',
                '192.168.32.0/19',
                '192.168.64.0/19',
                '192.168.96.0/19',
                '192.168.128.0/19']),
            '192.168.160.0/19'
        )

class TestMaximiseSubnets(unittest.TestCase):
    def test_maximise_subnets(self):
        self.assertEqual(
            maximise_subnets('192.168.0.0/16', 2),
            ['192.168.0.0/18',
            '192.168.64.0/18']
        )
        self.assertEqual(
            maximise_subnets('192.168.0.0/16', 3),
            ['192.168.0.0/18',
            '192.168.64.0/18',
            '192.168.128.0/18']
        )
        self.assertEqual(
            maximise_subnets('192.168.0.0/16', 5),
            ['192.168.0.0/19',
            '192.168.32.0/19',
            '192.168.64.0/19',
            '192.168.96.0/19',
            '192.168.128.0/19']
        )

class TestCalculateSubnets(unittest.TestCase):
    def test_calculate_subnets(self):
        self.assertEqual(
            calculate_subnets('192.168.0.0/16', 2),
            ['192.168.0.0/18',
            '192.168.64.0/18',
            '192.168.128.0/19',
            '192.168.160.0/19']
        )
        self.assertEqual(
            calculate_subnets('192.168.0.0/16', 3),
            ['192.168.0.0/18',
            '192.168.64.0/18',
            '192.168.128.0/18',
            '192.168.192.0/20',
            '192.168.208.0/20',
            '192.168.224.0/20']
        )
        self.assertEqual(
            calculate_subnets('192.168.0.0/16', 5),
            ['192.168.0.0/19',
            '192.168.32.0/19',
            '192.168.64.0/19',
            '192.168.96.0/19',
            '192.168.128.0/19',
            '192.168.160.0/22',
            '192.168.164.0/22',
            '192.168.168.0/22',
            '192.168.172.0/22',
            '192.168.176.0/22']
        )

if __name__ == '__main__':
    unittest.main()
