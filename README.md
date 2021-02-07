# foxholewar

A python wrapper for the foxhole [war api](https://github.com/clapfoot/warapi)

## Usage

```python
from foxholewar import foxholewar

# get the list of maps
maps = foxholewar.getMapList()

# print the current war number
war = foxholewar.getCurrentWar()
print(war.warNumber)

```

This is just a bit of fun and practice for me. Contributions welcome, and feel free to request any additions or changes
