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
TELEPORT_COLOR = np.array([0.,1.,0.]) # GREEN
LOGGER = logging.getLogger("gym-explorer")

class Explorer(gym.Env):

    def __init__(self, map):
        _map = utils.search(map)
        if _map is None:
            raise FileNotFoundError("Failed to find map file: {0}".format(map))
        map = _map

        #LOGGER.error("FOUND MAP FILE: {0}".format(map))
        
        image = Image.open(map)
        if image.mode == "RGBA": # convert to RGB... 
            _image = Image.new("RGB", image.size, (255, 255, 255))
            _image.paste(image, mask = image.split()[3])
            image = _image

        initial_state = np.array(image, dtype=np.float32).transpose(2,0,1) / 255.

        self.initial_player_position = None 
        self.initial_goal_position = None
        self.initial_teleport_positions = []

        self.state = np.copy(initial_state)

        self.viewer = None # for rendering

        #assume RGB format
        obj_pos = np.where(initial_state.sum(axis=0) == 1)

        #LOGGER.error(self.initial_state.shape)
        #LOGGER.error(self.initial_state.sum(axis=0))

        #assert len(obj_pos[0]) <= 2 # too many players or goals...

        for x,y in zip(*obj_pos):
            if np.all(initial_state[:,x,y] == PLAYER_COLOUR):
                self.initial_player_position = np.array([x,y])
            elif np.all(initial_state[:,x,y] == GOAL_COLOUR):
                self.initial_goal_position = np.array([x,y])
            elif np.all(initial_state[:,x,y] == TELEPORT_COLOR):
                self.initial_teleport_positions.append(np.array([x,y]))
            
        self.player_position = np.copy(self.initial_player_position)
        self.goal_position = np.copy(self.initial_goal_position)

        if self.player_position is None:
            raise ValueError("Failed to find player position.")
        if self.goal_position is None:
            raise ValueError("Failed to find goal position.")
       
        LOGGER.info(" -- GRID SIZE:", initial_state.shape)
        LOGGER.info(" -- PLAYER POSITION:", self.player_position)
        LOGGER.info(" -- GOAL POSITION:", self.goal_position)

        self.observation_space = gym.spaces.Box(np.float32(0), np.float32(1), shape=initial_state.shape, dtype=np.float32)
        self.physics = np.array([[-1,0],[0,1],[1,0],[0,-1],[0,0]], dtype=np.int64)
        self.action_space = gym.spaces.Discrete(self.physics.shape[0])
        self.mask = (self.state.sum(0) - 1) < 0 # wall mask 

    def get_action_meanings(self):
        return ["NORTH", "EAST", "SOUTH", "WEST", "NOOP"]

    def step(self, action):
        if self.is_done():
            return np.copy(self.state), 1., True, self.player_position.copy()
        pp = self.player_position
        npp = self.player_position + self.physics[action]

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
        return np.copy(self.state), 0, False, self.player_position.copy()

    def is_teleport(self, position):
        return len(self.initial_teleport_positions) > 0 and np.any(np.all(position == np.array(self.initial_teleport_positions), axis=1))

    def is_wall(self, position):
        return self.mask[position[0],position[1]]

    def is_done(self):
        return np.all(self.player_position == self.goal_position)

    def _replace_color(self, position):
        if np.all(position == self.goal_position):
            return GOAL_COLOUR
        elif self.is_teleport(position):
            return TELEPORT_COLOR
        return 1-float(self.mask[position[0],position[1]])

    def reset(self):
        pp = self.player_position
        self.state[:,pp[0],pp[1]] = self._replace_color(pp)
        self.player_position = np.copy(self.initial_player_position)
        self.goal_position = np.copy(self.initial_goal_position)
        npp = self.player_position
        self.state[:,npp[0],npp[1]] = PLAYER_COLOUR
        
        return np.copy(self.state), self.player_position.copy()

    def render(self, *args, **kwargs):
        if self.viewer is None: # first time setup
            self.viewer = view.ExplorerViewer(*args, **kwargs)
        self.viewer.render(self.state, *args, **kwargs)

    