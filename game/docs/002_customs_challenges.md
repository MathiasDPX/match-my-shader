# Customs challenges

To extend gameplay, you can install custom challenges in the configuration folder

- Linux: ~/.local/share/match_my_shader
- Windows: C:\Users\USERNAME\AppData\Local\mathias\match_my_shader

Custom challenges use Python like the code you write in the editor, however, you will add to have an headers and put the code in a function to make it valid

Here's an example challenge:

```
HEADERS = {
    "title": "Orpheus face", # Title in challenge list
    "starter": 'The code that will be in the editor after selecting the challenge', # Optional
    "size": (16, 16), # Canva size

    "_author": "orpheus" # Optional
}

def run(x,y):
    return (255, 0, 0)
```

I recommend you to store challenges in a dedicated folder for keeping your folder organized