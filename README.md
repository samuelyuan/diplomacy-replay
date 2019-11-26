# diplomacy-replay
Generate GIF replays of webDiplomacy games.

You can view the game replay as a GIF by combining the maps for each turn

```
python create_reply.py [gameID] [maxTurns] [largeMode]
```

For example, you want to view game 258084 which ended on turn 21:

```
python create_reply.py 258084 21 False
```

<div style="display:inline-block;">
<img src="https://github.com/samuelyuan/diplomacy-replay/raw/master/examples/game258084.gif" alt="example" width="400" height="300" />
</div>