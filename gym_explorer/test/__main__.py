#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 12-01-2021 16:50:34

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import h5py
import os
import numpy as np

import gym
import pygame
import gym_pygame
from gym_pygame.envs.pygame import KeyboardPolicy
gym_pygame.render() # must be before gym_explorer import

import gym_explorer

def file_checkpoint(path):
    file_num = lambda f: int(os.path.splitext(f)[0][8:])
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.startswith("episode-")]
    if len(files) == 0:
        return 0
    files = list(sorted(files, key=file_num))
    return file_num(files[-1])

def save(path, **data):
    # create new episode
    global FILE_CHECKPOINT
    FILE_CHECKPOINT += 1
    path = os.path.join(path, "episode-{0}.hdf5".format(FILE_CHECKPOINT))

    hf = h5py.File(path, 'w')
    for k,v in data.items():
        hf.create_dataset(k, data=v)
    hf.close()

MAP = "map1.png"
PATH = os.path.join("./data/human/", os.path.splitext(MAP)[0])
PATH = os.path.abspath(PATH)
FILE_CHECKPOINT = file_checkpoint(PATH)

if not os.path.exists(PATH):
    os.makedirs(PATH)

print("SAVING DATA TO: {0}".format(PATH))
print("RESUMING SAVE AT FILE: {0}".format(FILE_CHECKPOINT))

env = gym.make("explorer-v0", map=MAP)

# save meta data
import json
with open(os.path.join(PATH, "config.json"), 'w') as f:
    json.dump(dict(map=MAP, state_shape=env.observation_space.shape, action_shape=(env.action_space.n,)), f)


print(env.get_action_meanings())
policy = KeyboardPolicy(env.action_space)
policy.action_map = [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_SPACE]




while True: 
        
    done = False
    states, actions, rewards = [], [], []

    env.reset()
    env.render()

    while not done:
        action = policy()
        state, reward, done, *_ = env.step(action)
        env.render()

        states.append(state)
        actions.append(action)
        rewards.append(reward)
        print(action, reward, done)

    save(PATH, 
        states=np.array(states), 
        actions=np.array(actions),
        rewards=np.array(rewards))