#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 16-04-2021 14:47:30

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import contextlib
with contextlib.redirect_stdout(None): # stupid welcome message...
    import pygame

import numpy as np

pygame.init()

class ExplorerViewer:

    def __init__(self, display_size=(480,480), *args, **kwargs):
        self.display = pygame.display.set_mode(display_size)
        self.display_size = np.array(display_size)
        self.pygame = pygame # pygame module...
        self.quit = False

    def render(self, state, wait=0, *args, **kwargs):
        if not self.quit:
            state = (state.transpose(2,1,0) * 255) # HWC for pygame
            surface = self.pygame.surfarray.make_surface(state)
            surface = self.pygame.transform.scale(surface, self.display_size)
            self.display.blit(surface, (0,0))
            self.pygame.display.update()
            if wait > 0:
                pygame.time.wait(wait)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    self.quit = True

            # TODO also render action and reward? maybe also other meta info
