#!/usr/bin/env python3
import re
import subprocess
import sys
import string
import unittest
from rando_cli.rando import generate_random_characters

class TestRando(unittest.TestCase):
    
    def test_digits(self):
        """Test random digit generation with [x] pattern."""
        result = generate_random_characters("[xx]")
        self.assertEqual(len(result), 2)
        self.assertTrue(result.isdigit())
    
    def test_lowercase(self):
        """Test random lowercase letter generation with [a] pattern."""
        result = generate_random_characters("[aaa]")
        self.assertEqual(len(result), 3)
        self.assertTrue(all(c in string.ascii_lowercase for c in result))
    
    def test_uppercase(self):
        """Test random uppercase letter generation with [A] pattern."""
        result = generate_random_characters("[AAA]")
        self.assertEqual(len(result), 3)
        self.assertTrue(all(c in string.ascii_uppercase for c in result))
        
    def test_mixed_formats(self):
        """Test mixed formats like [a][x][A]."""
        result = generate_random_characters("[a][x][A]")
        self.assertEqual(len(result), 3)
        self.assertTrue(result[0] in string.ascii_lowercase)
        self.assertTrue(result[1].isdigit())
        self.assertTrue(result[2] in string.ascii_uppercase)
    
    def test_alternating_case(self):
        """Test mixed case in the same bracket like [aA]."""
        result = generate_random_characters("[aA][aA]")
        self.assertEqual(len(result), 4)
        for i in range(4):
            if i % 2 == 0:
                self.assertTrue(result[i] in string.ascii_lowercase)
            else:
                self.assertTrue(result[i] in string.ascii_uppercase)
    
    def test_text_with_formats(self):
        """Test text with embedded formats."""
        result = generate_random_characters("prefix-[xx]-middle-[aA]-suffix")
        parts = result.split('-')
        self.assertEqual(parts[0], "prefix")
        self.assertEqual(len(parts[1]), 2)
        self.assertTrue(parts[1].isdigit())
        self.assertEqual(parts[2], "middle")
        self.assertEqual(len(parts[3]), 2)
        self.assertTrue(parts[3][0] in string.ascii_lowercase)
        self.assertTrue(parts[3][1] in string.ascii_uppercase)
        self.assertEqual(parts[4], "suffix")

if __name__ == "__main__":
    unittest.main()