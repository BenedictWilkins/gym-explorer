#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 08-09-2020 16:28:49

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

from .. import utils

import gym
import numpy as np
import logging

from PIL import Image
from .explorer import Explorer, PLAYER_COLOUR

try: 
    from .. import view 
except ModuleNotFoundError:
    # pygame isnt installed, so we can't render
    view = None

# TODO make this a wrapper!
class BugExplorer(Explorer):

    def __init__(self, map):
        super().__init__(map)
        self.bugs = []

        self.physics = np.array([[-1,0],[0,1],[1,0],[0,-1]], dtype=np.int64) #  no noop actions
        self.action_space = gym.spaces.Discrete(self.physics.shape[0])
        
    def get_action_meanings(self):
        return ["NORTH", "EAST", "SOUTH", "WEST"]


    def step(self, action):
        bug = 0
        if self.is_done():
            return np.copy(self.state), 1., True, np.array([*self.player_position.copy(), bug])
        pp = self.player_position
        npp = self.player_position + self.physics[action] 
        if tuple(npp) in self.bugs: # if we are moving into a wall with a bug, skip through it!
            npp = npp + self.physics[action]
            bug = not self.is_wall(npp) # only a bug if we succeed in skipping through it!
        
        if self.is_out_of_bounds(npp): # there is a bug, we are going out of bounds!
            self.state[:,pp[0],pp[1]] = self._replace_color(pp)
            # self.state[:,npp[0],npp[1]] = PLAYER_COLOUR # the player disappears off the screen and the episode ends (in a crash!)
            #print("OUT OF BOUNDS", pp, npp)
            return np.copy(self.state), 0, True, np.array([*self.player_position.copy(), bug])

        if self.is_teleport(npp):
            self.state[:,pp[0],pp[1]] = self._replace_color(pp)
            i = (1 - np.all(npp == np.array(self.initial_teleport_positions), axis=1)).astype(bool) # select from
            _i = np.random.choice(np.arange(len(self.initial_teleport_positions))[i], size=1)[0]
            _npp = np.array(self.initial_teleport_positions)[_i]
            #print(pp, npp, self.initial_teleport_positions, _npp, i, _i,np.arange(len(self.initial_teleport_positions))[i])
            self.state[:,_npp[0],_npp[1]] = PLAYER_COLOUR
            self.player_position = _npp
        elif not self.is_wall(npp): #there is not a wall
            self.state[:,pp[0],pp[1]] = self._replace_color(pp)
            self.state[:,npp[0],npp[1]] = PLAYER_COLOUR
            self.player_position = npp
        return np.copy(self.state), 0, False, np.array([*self.player_position.copy(), bug])

    def is_out_of_bounds(self, position):
        return np.any(position < 0) or position[0] >= self.state.shape[1] or position[1] >= self.state.shape[2]

    def reset(self):
        pp = self.player_position
        self.state[:,pp[0],pp[1]] = self._replace_color(pp)
        self.player_position = np.copy(self.initial_player_position)
        self.goal_position = np.copy(self.initial_goal_position)
        npp = self.player_position
        self.state[:,npp[0],npp[1]] = PLAYER_COLOUR
        
        return np.copy(self.state), np.array([*self.player_position.copy(), 0])

    def is_done(self):
        return False

    def set_bugs(self, bugs):
        self.bugs = [tuple(bug) for bug in bugs]