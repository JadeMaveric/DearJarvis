# -*- coding: utf-8 -*-
import unittest
import logging

from gkeepapi import node

logging.getLogger(node.__name__).addHandler(logging.NullHandler())

def generate_save_load(cls):
    """Constructs an empty object and clones it from the serialized representation."""

class AnnotationTests(unittest.TestCase):
    def test_save_load(self):
        a, b = generate_save_load(node.Annotation)
        self.assertEqual(a, b)
