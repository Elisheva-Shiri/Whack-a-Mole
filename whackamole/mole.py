# -*- coding: utf-8 -*-

"""
Whack a Mole
~~~~~~~~~~~~~~~~~~~
A simple Whack a Mole game written with PyGame
"""

from random import randint, choice
from pygame import image, transform, time, mixer
from .lightMatrix import LightMatrix
from .constants import ImageConstants, MoleConstants, LevelConstants, HoleConstants


class Mole:
    """
    Provides the mole used in game
    """

    def __init__(self, light_matrix: LightMatrix):
        # Load images
        self.img_normal = image.load(ImageConstants.IMAGEMOLENORMAL)
        self.img_normal = transform.scale(self.img_normal, (MoleConstants.MOLEWIDTH, MoleConstants.MOLEHEIGHT))
        self.img_hit = image.load(ImageConstants.IMAGEMOLEHIT)
        self.img_hit = transform.scale(self.img_hit, (MoleConstants.MOLEWIDTH, MoleConstants.MOLEHEIGHT))

        # State of showing animation
        # 0 = No, 1 = Doing Up, -1 = Doing Down
        self.showing_state = 0

        # Hold timestamp for staying up
        self.showing_counter = 0

        # Hold how long mole will stay up
        self.show_time = 0

        # Our current hole data
        self.current_hole = (0, 0)
        self.last_hole = (0, 0)
        self.position = -1

        # Current frame of showing animation
        self.show_frame = 0

        # Total number of frames to show for popping up (not timed)
        self.frames = 5

        # Cooldown from last popup
        self.cooldown = 0

        # Indicates if mole is hit
        # False = Not hit, timestamp for stunned freeze
        self.hit = False

        # save lightMatrix
        self.light_matrix = light_matrix

    @property
    def image(self):
        if self.hit != False: return self.img_hit
        return self.img_normal

    def chance(self, level):
        level -= 1  # Start at 0

        levelChance = 1 + ((LevelConstants.LEVELMOLECHANCE / 100) * level)

        chance = int((MoleConstants.MOLECHANCE ** -1) * levelChance)
        return chance

    def timeLimits(self, level):
        level -= 1  # Start at 0

        levelTime = 1 - ((LevelConstants.LEVELMOLESPEED / 100) * level)
        if levelTime < 0: levelTime = 0  # No wait, just up & down

        timeMin = int(MoleConstants.MOLEUPMIN * 1000 * levelTime)
        timeMax = int(MoleConstants.MOLEUPMAX * 1000 * levelTime)

        return (timeMin, timeMax)

    def do_display(self, holes, level, do_tick=True):
        # If in cooldown
        if self.cooldown != 0:
            if time.get_ticks() - self.cooldown < MoleConstants.MOLECOOLDOWN:
                return [False]
            else:
                self.cooldown = 0
                return [False, 1, self.last_hole]

        # If doing a tick
        if do_tick:

            # Random choice if not showing
            new_hole = False
            if self.showing_state == 0 and holes:
                # Reset
                self.show_frame = 0
                self.hit = False

                # Pick
                random = randint(0, self.chance(level))
                if random == 0:
                    self.showing_state = 1
                    self.showing_counter = 0

                    self.show_time = randint(*self.timeLimits(level))

                    # Pick a new hole, don't pick the last one, don't infinite loop
                    self.current_hole = self.last_hole
                    if len(holes) > 1 or self.current_hole != holes[0]:
                        self.light_matrix.lightOff(self.position)
                        while self.current_hole == self.last_hole:  # as long as the holes are the same pick a new one
                            self.position = randint(0, len(holes)-1)  # define a new position in the class
                            self.current_hole = holes[self.position]  # use the same position to keep the hole
                        self.last_hole = self.current_hole
                        self.light_matrix.lightOn(self.position)
                        new_hole = True

            # Show as popped up for a bit
            if self.showing_state == 1 and self.showing_counter != 0:
                if time.get_ticks() - self.showing_counter >= self.show_time:
                    self.showing_state = -1
                    self.showing_counter = 0

            # Return if game should display, including new hole data
            if new_hole:
                return [True, 0, self.current_hole]

        # Return if game should display
        return [(not self.showing_state == 0)]

    def get_base_pos(self):
        holeX, holeY = self.current_hole
        offset = (HoleConstants.HOLEWIDTH - MoleConstants.MOLEWIDTH) / 2

        moleX = holeX + offset
        moleY = (holeY + HoleConstants.HOLEHEIGHT) - (MoleConstants.MOLEHEIGHT * 1.2)
        return (moleX, moleY)

    def get_hole_pos(self, do_tick=True):
        moleX, moleY = self.get_base_pos()

        frame = 0

        # Stunned
        if self.hit != False:
            if time.get_ticks() - self.hit >= MoleConstants.MOLESTUNNED:
                # Unfrozen after hit, hide
                if self.showing_state != 0:
                    self.showing_state = -1
            else:
                # Frozen from hit
                do_tick = False

        # Going Up
        if self.showing_state == 1:
            if self.show_frame <= self.frames:
                frame = MoleConstants.MOLEDEPTH / self.frames * (self.frames - self.show_frame)
                if do_tick: self.show_frame += 1
            else:
                # Hold
                if self.showing_counter == 0:
                    self.showing_counter = time.get_ticks()

        # Going Down
        if self.showing_state == -1:
            if do_tick: self.show_frame -= 1
            if self.show_frame >= 0:
                frame = MoleConstants.MOLEDEPTH / self.frames * (self.frames - self.show_frame)
            else:
                # Reset
                self.showing_state = 0
                frame = MoleConstants.MOLEDEPTH
                # Begin cooldown
                if do_tick: self.cooldown = time.get_ticks()

        moleY += (MoleConstants.MOLEHEIGHT * (frame / 100))

        return (moleX, moleY)

    def is_hit(self, pos):
        if pos == self.position:   # if mole gut hit
            if self.hit is False:  # if mole didn't gut hit yet
                self.hit = time.get_ticks()  # keep the time when the mole gut hit
                return 1
            else:
                return 2

        return False
