#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 08-09-2020 16:52:02

    Some useful functions.
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import os

def maps():
    path = os.path.split(__file__)[0] 
    path = os.path.join(path, 'maps')
    files = [os.path.join(path, f) for f in os.listdir(path)] 
    return files

def search(file):
    """ Find a map file.
        Search order:
            absolute path (if applicable) 
            current working directory
            gym_exploers/maps/
    Args:
        file (str): file name or path

    Returns:
        str: absolute file path
    """
    _file = os.path.abspath(file) # attempt to get the absolute path
    if os.path.isfile(_file):
        return _file
    
    # search default files
    for default_file in maps():
        _default_file = os.path.split(default_file)[1]
        if file == _default_file:
            return default_file
    
    return None # no file was found ...