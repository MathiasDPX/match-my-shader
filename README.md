# Match my Shader

"Match my Shader" is a creative programming game where you write Python code to recreate shaders and match pixel-perfect results. This game was made in 10 days for the "Timeless" game jam hosted by Lux

## 🎮 About the Game

In Match my Shader, your challenge is to write Python code that renders a shader to match a given target output pixel-perfectly

A shader is a small program that runs in parallel for every pixel and decides its color, which means you have to write one code for the whole image

The game features two main modes:
- **Freeplay**: Code freely for fun or to draw creative designs
- **Challenge**: Recreate exactly a given target shader

## 📦 Installation

## 🏃 Run 
```bash
python -m pip install -r requirements.txt
cd game
python main.py
```

## 🔨 Build

To create a standalone executable:

**Windows:**
```bash
build.bat
```

**Linux:**
```bash
chmod +x build.sh
./build.sh
```

The executable will be generated in the `game/dist/` folder.

## 🎯 How to Play

1. **Select a Challenge**: Click "Challenges" to see the list
2. **Write your code**: Your function should return a color for each pixel (x, y)
3. **Repeat**

If you need help using the game, you can open the Help menu on the menubar

## 🏆 "Timeless" Game Jam

This project was created for the "Timeless" game jam with the goal of building a game that could be enjoyed for the next 10 years. The concept of creative programming and learning aligns perfectly with this vision of timelessness.