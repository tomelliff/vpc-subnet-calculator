#!/usr/bin/env python
import unittest
import sys

from mock import patch

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

    def test_minimum_subnet_size(self):
        with self.assertRaises(ValueError) as e:
            maximise_subnets('192.168.0.0/28', 2)

        self.assertTrue('Minimum subnet size is /28' in e.exception)

    def test_maximum_subnet_size(self):
        with self.assertRaises(ValueError) as e:
            maximise_subnets('10.0.0.0/8', 2)

        self.assertTrue('Maximum subnet size is /16' in e.exception)


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


class TestCommandLineInterface(unittest.TestCase):
    def test_arg_parser(self):
        sys.argv[1] = '192.168.0.0/16'
        sys.argv.append('5')
        self.assertEqual(arg_parser(), ('192.168.0.0/16', 5))

    @patch('__builtin__.print')
    @patch('vpc_subnet_calculator.arg_parser',
           return_value=('192.168.0.0/16', 2))
    @patch('vpc_subnet_calculator.calculate_subnets',
           return_value=['192.168.0.0/18'
                         '192.168.64.0/18'
                         '192.168.128.0/19'
                         '192.168.160.0/19'])
    def test_main(self, mock_calculate_subnets, mock_arg_parser, mock_print):
        main()
        mock_calculate_subnets.assert_called_once_with(
            '192.168.0.0/16', 2)
        # Looped prints seem to get concatenated
        # rather than called multiple times
        mock_print.assert_called_with(
            '192.168.0.0/18192.168.64.0/18192.168.128.0/19192.168.160.0/19')


if __name__ == '__main__':
    unittest.main()
