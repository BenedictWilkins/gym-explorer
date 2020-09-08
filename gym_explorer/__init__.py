import os
from gym.envs.registration import register

from . import envs
from .utils import maps

_all__ = ('envs', )

register(
    id='explorer-v0',
    entry_point='gym_explorer.envs:Explorer'
)

