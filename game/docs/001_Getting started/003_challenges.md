# Challenge mode

Challenge mode is the heart of Match my Shader. Your aim is to reproduce a target image exactly by writing Python code.

To start a Challenge :
1. Click on "Challenges" in the menu bar
2. Select a challenge
3. Start coding in the editor

Scoring :
- Score is based on the number of tokens in your code
- Less tokens = better score

Customs challenges: You may want to add some customs challenges with flags, profile picture & more, it fully possible with this game!

First, you need to find the data folder on your computer:
- Windows: `C:\Users\USERNAME\AppData\Local\mathias\match_my_shader`
- Linux: `~/.local/match_my_shader`

Inside there is a `challenges` folder, every .py files inside while be considered a challenge (including files in subfolders), here's an example challenge (taken from the first challenge)

```python
HEADERS = {
    "title": "Title",
    "starter": '# Code that will be in the editor when starting the challenge',
    "size": (16, 16),

    "_author": "@orpheus"
}

def run(x,y):
    return (255, 0, 0)
```

If you want to add a palette, simply add a key named `palette` assigned to a list of colors like this:

```
"palette": [0x000000, (123,123,123), (128,128,128,128)]
```

note that palette support every type of colors