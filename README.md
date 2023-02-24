# Miragine Advisor

## Introduction

A simple python project to play Miragine War based on hard rules and some calculations. Can beat hard mode almost for sure, but is still helpless confronted with the abyss mode.

Please notice that this program is only for the oldest **Flash** version of Miragine war.

## The Game

I found a free online version [here](https://gamefilez.mofunzone.com/gamefilez/miragine.swf?1306481903). Click to have fun!

If you are too unlucky to open the link above, I have the flash version `miragine.swf` for you to play (it's also from the link above).

## How to Use

Be sure to have python and `pip install -r requirements.txt` before you download this project. First run `generate_strategies.ipynb` to generate your strategies in the `data` folder. Then simply run `main.ipynb` after you start the game, and the program will automatically click the best army to fight the opponent.

You may encounter wrong clicks due to the different size of your screen. Please open the `utils/Reaction.py` and change the **pos_map**, **area_map** and **grab_area**. You may also need to change the **grab_area** in `main.ipynb`.

If you want to **stop** the program, just randomly move your mouse and the program will crash due to the pyautogui protection (sorry I did not take pains to find a way to elegantly shut down the program, after all it's just a toy haha).

Please forgive me for some Chinese annotations in the files (or English annotations if you are a Chinese).
