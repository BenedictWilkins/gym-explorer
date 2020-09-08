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
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    return files

def search(file):
    """  
        Find a map file.

        Search order:
            absolute path (if applicable) 
            current working directory
            gym_exploers/maps/
        
    Args:
        file (str): file name or path

    Returns:
        str: absolute file path
    """
    if os.path.isfile(file):
        return file

    cwd = os.getcwd()
    if file in os.listdir(cwd):
        return os.path.join(cwd, file)

    if file in maps():
        path = os.path.split(__file__)[0] 
        path = os.path.join(path, 'maps')
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
        return os.path.join(path, file)