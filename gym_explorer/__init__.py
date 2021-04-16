#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 16-04-2021 15:43:38

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import os
import gym.envs.registration
from gym import make

from . import envs
from . import utils

__ENVIRONMENTS__ = []

def register(file):
    path = utils.search(file)
    map_name = os.path.splitext(os.path.split(map)[1])[0]
    env_id = 'explorer-{0}-v0'.format(map_name)
    gym.envs.registration.register(id=env_id, entry_point='gym_explorer.envs:Explorer', kwargs=dict(map=path))
    __ENVIRONMENTS__.append(env_id)

try: 
    from . import view 
    __all__ = ('envs', 'utils', 'view')
except ModuleNotFoundError:
    # pygame isnt installed, so we can't render
    view = None
    __all__ = ('envs', 'utils')

# register all the default environments
for map in utils.maps():
    register(map)

gym.envs.registration.register(id="explorer-v0", entry_point='gym_explorer.envs:Explorer')

def environments():
    return [e for e in __ENVIRONMENTS__]
