# -*- coding: utf-8 -*-

"""
Whack a Mole
~~~~~~~~~~~~~~~~~~~
A simple Whack a Mole game written with PyGame
:copyright: (c) 2018 Matt Cowley (IPv4)
"""

"""Search for '# !!' in the file to find the most common constant to change."""


class GameConstants:
    """
    Constants used for rendering of main game
    """

    GAMEWIDTH       = 500
    GAMEHEIGHT      = 500
    GAMEMAXFPS      = 60


class LevelConstants:
    """
    Constants used to handle leveling
    """

    LEVELGAP        = 10 #score
    LEVELMOLESPEED  = 5 #% faster
    LEVELMOLECHANCE = 10 #% less


class HoleConstants:
    """
    Constants used in the holes
    """

    HOLEWIDTH       = 100
    HOLEHEIGHT      = int(HOLEWIDTH*(3/8))
    HOLEROWS        = 3 # !!
    HOLECOLUMNS     = 3 # !!

    # Checks
    if HOLEHEIGHT*HOLEROWS > GameConstants.GAMEHEIGHT:
        raise ValueError("HOLEROWS or HOLEHEIGHT too high (or GAMEHEIGHT too small)")
    if HOLEWIDTH*HOLECOLUMNS > GameConstants.GAMEWIDTH:
        raise ValueError("HOLECOLUMNS or HOLEWIDTH too high (or GAMEWIDTH too small)")

class BoardConstants:
    """
    Constants used to difine pinout
    """

    PINS        = [2, 3, 4, 17, 27, 22, 10, 9, 11]
    BUTTON_PINS = [14, 15, 18, 23, 24, 25, 8, 7, 12]

class MoleConstants:
    """
    Constants used for mole generation and calculations
    """

    MOLEWIDTH       = int( HoleConstants.HOLEWIDTH*(2/3) )
    MOLEHEIGHT      = int(MOLEWIDTH)
    MOLEDEPTH       = 15 #% of height
    MOLECOOLDOWN    = 500 #ms

    MOLESTUNNED     = 1000 #ms
    MOLEHITHUD      = 500 #ms
    MOLEMISSHUD     = 250 #ms

    MOLECHANCE      = 1/30
    MOLECOUNT       = 1  # Amount of moles, one mole so all holes are open each time. otherwise the keypress fails (position-hole mismatch)
    MOLEUPMIN       = 0.3 #s
    MOLEUPMAX       = 2 #s

    # Checks
    if MOLECOUNT > HoleConstants.HOLEROWS*HoleConstants.HOLECOLUMNS:
        raise ValueError("MOLECOUNT too high")


class TextConstants:
    """
    Constants used for text rendering
    """

    TEXTTITLE       = "Whack a Mole"
    TEXTFONTSIZE    = 15
    TEXTFONTFILE    = "assets/OxygenMono-Regular.ttf"


class ImageConstants:
    """
    Constants that are image based
    """

    IMAGEBASE       = "assets/"

    IMAGEBACKGROUND = IMAGEBASE + "background.png"

    IMAGEMOLENORMAL = IMAGEBASE + "mole.png"
    IMAGEMOLEHIT    = IMAGEBASE + "mole_hit.png"

    IMAGEHOLE       = IMAGEBASE + "hole.png"
    IMAGEMALLET     = IMAGEBASE + "mallet.png"


class MalletConstants:
    """
    Constants used for rendering the mallet
    """

    MALLETWIDTH     = int(HoleConstants.HOLEWIDTH)
    MALLETHEIGHT    = int(MALLETWIDTH)

    MALLETROTNORM   = 15
    MALLETROTHIT    = 30


class Constants(GameConstants, LevelConstants, HoleConstants, BoardConstants, MoleConstants, TextConstants, ImageConstants, MalletConstants):
    """
    Stores all the constants used in the game
    """

    DEBUGMODE       = False
    LEFTMOUSEBUTTON = 1

