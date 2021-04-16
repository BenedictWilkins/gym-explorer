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

try: 
    from .. import view 
except ModuleNotFoundError:
    # pygame isnt installed, so we can't render
    view = None

PLAYER_COLOUR = np.array([1.,0.,0.]) # RED
GOAL_COLOUR = np.array([0.,0.,1.])   # BLUE
LOGGER = logging.getLogger("gym-explorer")

class Explorer(gym.Env):

    def __init__(self, map):
        _map = utils.search(map)
        if _map is None:
            raise FileNotFoundError("Failed to find map file: {0}".format(map))
        map = _map

        LOGGER.info("FOUND MAP FILE: ", map)

        self.initial_state = np.array(Image.open(map), dtype=np.float32).transpose(2,0,1) / 255.
        self.initial_player_position = None 
        self.initial_goal_position = None

        self.state = np.copy(self.initial_state)

        self.viewer = None # for rendering

        #assume RGB format
        obj_pos = np.where(self.initial_state.sum(axis=0) == 1)
        assert len(obj_pos[0]) <= 2 # too many players or goals...

        for x,y in zip(*obj_pos):
            if np.all(self.initial_state[:,x,y] == PLAYER_COLOUR):
                self.initial_player_position = np.array([x,y])
            elif np.all(self.initial_state[:,x,y] == GOAL_COLOUR):
                self.initial_goal_position = np.array([x,y])

        self.player_position = np.copy(self.initial_player_position)
        self.goal_position = np.copy(self.initial_goal_position)

        if self.player_position is None:
            raise ValueError("Failed to find player position.")
        if self.goal_position is None:
            raise ValueError("Failed to find goal position.")
       
        LOGGER.info(" -- GRID SIZE:", self.initial_state.shape)
        LOGGER.info(" -- PLAYER POSITION:", self.player_position)
        LOGGER.info(" -- GOAL POSITION:", self.goal_position)

        self.observation_space = gym.spaces.Box(np.float32(0), np.float32(1), shape=self.initial_state.shape, dtype=np.float32)
        self.physics = np.array([[-1,0],[0,1],[1,0],[0,-1],[0,0]], dtype=np.int64)
        self.action_space = gym.spaces.Discrete(self.physics.shape[0])
        self.mask = (self.state.sum(0) - 1) < 0 # wall mask 

    def get_action_meanings(self):
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
        if self.viewer is None: # first time setup
            self.viewer = view.ExplorerViewer(*args, **kwargs)
        self.viewer.render(self.state, *args, **kwargs)

    