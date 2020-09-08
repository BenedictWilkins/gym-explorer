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
from PIL import Image

PLAYER_COLOUR = np.array([1.,0.,0.]) # RED
GOAL_COLOUR = np.array([0.,0.,1.])   # BLUE


class Explorer(gym.Env):

    def __init__(self, map, verbose=True):
        map = utils.search(map)

        if verbose:
            print("FOUND MAP FILE: ", map)

        self.initial_state = np.array(Image.open(map), dtype=np.float32).transpose(2,0,1) / 255.
        self.initial_player_position = None 
        self.initial_goal_position = None

        self.state = np.copy(self.initial_state)

        #assume RGB format
        obj_pos = np.where(self.initial_state.sum(axis=0) == 1)
        assert len(obj_pos[0]) <= 2 # too many players or goals...

        for x,y in zip(*obj_pos):
            if np.all(self.initial_state[:,x,y] == PLAYER_COLOUR):
                self.initial_player_position = np.array([y,x])
            elif np.all(self.initial_state[:,x,y] == GOAL_COLOUR):
                self.initial_goal_position = np.array([y,x])


        self.player_position = np.copy(self.initial_player_position)
        self.goal_position = np.copy(self.initial_goal_position)

        if self.player_position is None:
            raise ValueError("Failed to find player position.")
        if self.goal_position is None:
            raise ValueError("Failed to find goal position.")
       
        if verbose:
            print(" -- GRID SIZE:", self.initial_state.shape)
            print(" -- PLAYER POSITION:", self.player_position)
            print(" -- GOAL POSITION:", self.goal_position)

        self.observation_space = gym.spaces.Box(np.float32(0), np.float32(1), shape=self.initial_state.shape, dtype=np.float32)
        self.physics = np.array([[-1,0],[0,1],[1,0],[0,-1],[0,0]], dtype=np.int64)
        self.action_space = gym.spaces.Discrete(self.physics.shape[0])
        self.mask = (self.state.sum(0) - 1) < 0 # wall mask 

    def action_meanings(self):
        return ["NORTH", "EAST", "SOUTH", "WEST", "NOOP"]

    def step(self, action):
        if np.all(self.player_position == self.goal_position):
            return np.copy(self.state), 1., True, None
        pp = self.player_position
        npp = self.player_position + self.physics[action] 
        if not self.mask[npp[0],npp[1]]: #there is not a wall
            self.state[:,pp[0],pp[1]] = 1.
            self.state[:,npp[0],npp[1]] = PLAYER_COLOUR
            
            self.player_position = npp
        return np.copy(self.state), 0, False, None

    def reset(self):
        self.player_position = np.copy(self.initial_player_position)
        self.goal_position = np.copy(self.initial_goal_position)
        self.state = np.copy(self.initial_state)
        return np.copy(self.state)

    def render(self, *args, **kwargs):
        pass
        