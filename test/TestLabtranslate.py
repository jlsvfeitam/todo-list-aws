#!/usr/local/bin/python
# coding: latin-1
import warnings
import unittest
import boto3
import sys
import os
import json


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        print ('---------------------')
        print ('Start: setUp')
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")
        print ('End: setUp')
    
    def test_translate(self):
        print ('---------------------')
        print ('Start: test_translate')
        from src.labtranslate import labtranslate
        
        responseTranslate = labtranslate('Hello')
        self.assertEqual(
            responseTranslate,
            'Hola')
        print ('End: test_translate')
        
    def test_translate2(self):
        print ('---------------------')
        print ('Start: test_translate2')
        from src.translatetext import translatetext
        
        responseTranslate = translatetext('Hello', 'en', 'es')
        self.assertEqual(
            responseTranslate,
            'Hola')
        print ('End: test_translate2')
    
if __name__ == '__main__':
    unittest.main()