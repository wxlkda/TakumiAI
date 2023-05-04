
# Takumi AI

## Overview
**Takumi AI** is a game I developed in 2022 using **PyGame**. It is a 2D runner game where the goal is to survive the longest while avoiding obstalces. As you progress through the game, the "speed of the player" increases, making it more difficult to avoid the obstalces. 

Takumi AI also features a **neural network mode**, where the AI gets trained on processing nodes called **neurons** that learns and recognizes **patterns** in the game. In Takumi AI, the "Train" mode starts off at generation 1 with **15 simulations** of the player at once. Once every single player on the screen dies, a new generation is created. In each generation, hidden layers of data gets applied to each simulated player. From this, the neurons then perform calculations and apply "weights" to the player, causing different actions such as jump, duck, or duck while jumping

![](https://i.ibb.co/tCpkzsh/Screenshot-2023-05-04-005343.png)
## Features

 - Use **Up** and **Down** arrows keys to navigate between Play and Train
 - Press **Enter** to confirm your selection
 - This game features 2 different modes: **Play** mode and **Train** mode. 
   
   In **Play** mode:
   
    - You get to play the game yourself. Press space to jump and down arrow key to go down mid air
    - The game gets progressively faster the higher your score
   
   In **Train** mode:
   
    - 15 simulated players are generated each model.
    - After all the players die in 1 generation, the next generation forms with new weights and hidden layer data
    - The AI has "succeeded" whenever it hits a score of 10,000. After 10,000, the speed of the game becomes too fast for even the AI to handle

## Set up

 1. Visit [the game repo on Github](https://github.com/wxlkda/littlerunner) and click "Code" in the top right corner to download the repository as a ZIP.
 2. Make sure you have Python installed. If not, install it from [this link](https://www.python.org/downloads/)
 3. If you do not have the PyGame framework installed, open a new terminal and run `python -m pip install --user pygame==2.1.2`
 4. After successfully installing, run the file "main.py". To run from terminal, do the following:
		  `cd <directory you installed the zip>` (Make sure this directory has the main.py file)
		  `python main.py`
 5. This should launch the game in a separate window. Press **esc** to close the game or follow the instructions above in order to play the game itself
