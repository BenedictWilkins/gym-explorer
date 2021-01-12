# gym-explorer
A simple customisable environment for testing explorative agents. 

The explorer environment is a grid-world in which a player moves around (NORTH,SOUTH,EAST,WEST) and attempts to reach a goal tile. The map can be specified as an image, with a red pixel representing the player, a blue pixel representing the goal, white pixels representy free tiles, and black pixels representing walls. The map is specified as below:
```
gym.make("explorer-v0", map="map1.png")
```


