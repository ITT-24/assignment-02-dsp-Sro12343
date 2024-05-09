A lot of the comments i created with Chatgpt, because it seamd easier, than to write them myself. They tend to have a space after the #
# AI_Generated_Comment
#Comments_written_by_me.


Karaoke:
!!! Headphones are advised, so sound does not interfere with input!!

The Game starts with karaoke.py

First, the input and output devices are set on the terminal. Then the game starts on the menu/title screen

With the up and down arrows, the players can switch between songs and start the game with the enter button. The Menu also plays the songs as a preview.

During the game, players sing/whistle the fitting notes. To the song. There are only 12 different notes in the input; different octaves are counted as the same note. As long as the notes are touched by the player/box, they become green and the player gains points. After the song returns to the menu and the achieved score is shown(in the Tetris song this takes some time, which has to do with the midi file, as the game waits for the midi file to be done),

The Tetris midi came from (https://bitmidi.com/tetris-tetris-main-theme-mid)

List of all imports:
import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import pyglet
from pyglet.window import key
import mido

from GameLogic import GameLogic
from MenuLogic import MenuLogic
from freqencyCalculator import FreqCalculator
from scipy import signal
import os.path
import threading
from MenuSongPlayer import songPlayer
from SingleNote import SingleNote
from Player import Player
from pyglet import shapes





Whistle input:
The whistle input can be started with whistle-input.py

A screen visualising the input changes opens.

Make a long whistle up or downards to make an input

A very long whistle makes multiple inputs







[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/iur3tfNd)
