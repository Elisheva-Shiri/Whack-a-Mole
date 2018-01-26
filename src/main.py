# -*- coding: utf-8 -*-

"""
Whack a Mole
~~~~~~~~~~~~~~~~~~~
A simple Whack a Mole game written with PyGame
:copyright: (c) 2018 Matt Cowley (IPv4)
"""

from pygame import init, quit, display, image, transform, time, mouse, event, QUIT, MOUSEBUTTONDOWN, KEYDOWN, \
    K_e, K_r, K_t, K_y, K_u, K_i, K_o, K_p
from src.constants import Constants
from src.mole import Mole
from src.text import Text
from src.score import Score


class Game:
    """
    Handles the main game
    """

    def __init__(self):
        # Init pygame
        init()

        # Create pygame screen
        self.screen = display.set_mode((Constants.GAMEWIDTH, Constants.GAMEHEIGHT))
        display.set_caption(Constants.TEXTTITLE)

        # Load background
        self.img_background = image.load(Constants.IMAGEBACKGROUND)
        self.img_background = transform.scale(self.img_background, (Constants.GAMEWIDTH, Constants.GAMEHEIGHT))

        # Load hole
        self.img_hole = image.load(Constants.IMAGEHOLE)
        self.img_hole = transform.scale(self.img_hole, (Constants.HOLEWIDTH, Constants.HOLEHEIGHT))

        # Load moles
        self.moles = [Mole() for _ in range(Constants.MOLECOUNT)]

        # Generate hole positions
        self.holes = []
        self.used_holes = []
        base_row = Constants.GAMEHEIGHT/Constants.HOLEROWS
        base_column = Constants.GAMEWIDTH/Constants.HOLECOLUMNS
        for row in range(Constants.HOLEROWS):
            rowY = base_row * row
            rowY += (base_row-Constants.HOLEHEIGHT)/2
            for column in range(Constants.HOLECOLUMNS):
                thisX =  base_column * column
                thisX += (base_column-Constants.HOLEWIDTH)/2
                self.holes.append((int(thisX), int(rowY)))

        # Get the text object
        self.text = Text()

        # Get the score object
        self.score = Score(self.text)

        # Indicates wether the HUD indicators should be displayed
        self.show_hit = 0
        self.show_miss = 0

    def loop_events(self):

        hit = False
        miss = False
        pos = mouse.get_pos()

        # Handle PyGame events
        for e in event.get():

            # Handle quit
            if e.type == QUIT:
                self.loop = False
                break

            # Handle click
            if e.type == MOUSEBUTTONDOWN and e.button == Constants.LEFTMOUSEBUTTON:
                miss = True
                for mole in self.moles:
                    if mole.is_hit(pos) == 1:  # Hit
                        hit = True
                        miss = False
                    if mole.is_hit(pos) == 2:  # Hit but stunned
                        miss = False

                if hit:
                    self.score.hit()
                if miss:
                    self.score.miss()

            # Handle cheats (for dev work)
            if Constants.DEBUGMODE and e.type == KEYDOWN:
                if e.key == K_e:
                    hit = True
                    missed = False
                    self.score.hit()
                if e.key == K_r:
                    hit = False
                    missed = True
                    self.score.miss()

                if e.key == K_t:
                    self.score.misses = 0
                if e.key == K_y:
                    self.score.misses += 5
                if e.key == K_u:
                    self.score.misses -= 5

                if e.key == K_i:
                    self.score.hits = 0
                if e.key == K_o:
                    self.score.hits += 5
                if e.key == K_p:
                    self.score.hits -= 5

        return (hit, miss)


    def loop_display(self, hit, miss):
        # Display bg
        self.screen.blit(self.img_background, (0, 0))

        # Display holes
        for position in self.holes:
            self.screen.blit(self.img_hole, position)

        # Display moles
        for mole in self.moles:
            holes = [f for f in self.holes if f not in self.used_holes]
            mole_display = mole.do_display(holes, self.score.level)

            # If new/old hole given
            if len(mole_display) > 1:
                if mole_display[1] == 0:  # New hole
                    self.used_holes.append(mole_display[2])
                else:  # Old hole
                    if mole_display[2] in self.used_holes:
                        self.used_holes.remove(mole_display[2])

            # If should display
            if mole_display[0]:
                # Get pos and display
                pos = mole.get_hole_pos()
                self.screen.blit(mole.image, pos)

        # Debug data for readout
        debug_data = {}
        if Constants.DEBUGMODE:
            debug_data = {
                "DEBUG": True,
                "FPS": int(self.clock.get_fps()),
                "MOLES": "{}/{}".format(Constants.MOLECOUNT, Constants.HOLEROWS * Constants.HOLECOLUMNS),
                "KEYS": "E[H]R[M]T[M0]Y[M+5]U[M-5]I[H0]O[H+5]P[H-5]"
            }

        # Display data readout
        data = self.score.label(debug_data)
        self.screen.blit(data, (5, 5))

        # Hit indicator
        if hit:
            self.show_hit = time.get_ticks()
        if self.show_hit > 0 and time.get_ticks() - self.show_hit <= Constants.MOLEHITHUD:
            hit_label = self.text.get_label("Hit!", scale=3, color=(255, 50, 0))
            hit_x = (Constants.GAMEWIDTH - hit_label.get_width()) / 2
            hit_y = (Constants.GAMEHEIGHT - hit_label.get_height()) / 2
            self.screen.blit(hit_label, (hit_x, hit_y))
        else:
            self.show_hit = 0

        # Miss indicator
        if miss:
            self.show_miss = time.get_ticks()
        if self.show_miss > 0 and time.get_ticks() - self.show_miss <= Constants.MOLEMISSHUD:
            miss_label = self.text.get_label("Miss!", scale=2, color=(0, 150, 255))
            miss_x = (Constants.GAMEWIDTH - miss_label.get_width()) / 2
            miss_y = (Constants.GAMEHEIGHT + miss_label.get_height()) / 2
            self.screen.blit(miss_label, (miss_x, miss_y))
        else:
            self.show_miss = 0

    def start(self):
        self.clock = time.Clock()
        self.loop = True

        while self.loop:

            # Do all events
            hit, miss = self.loop_events()

            # Do all render
            self.loop_display(hit, miss)

            # Update display
            self.clock.tick(Constants.GAMEMAXFPS)
            display.flip()

    def run(self):
        self.start()
        quit()