#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import DISPLAY_WIDTH, TFT


class DrawString:

    def __init__(self, string, font, color, y):

        """
        :param string: the input string
        :param font: the font object
        :param color: a rgb color tuple
        :param y: the y position where you want to render the text
        """
        self.string = string
        self.font = font
        self.color = color
        self.y = y
        self.size = self.font.size(self.string)

    def left(self, offset=0):

        """
        :param offset: define some offset pixel to move strings a little bit (default=0)
        :return:
        """

        x = 10 + offset

        self.draw_string(x)

    def right(self, offset=0):

        """
        :param offset: define some offset pixel to move strings a little bit (default=0)
        :return:
        """

        x = (DISPLAY_WIDTH - self.size[0] - 10) - offset

        self.draw_string(x)

    def center(self, parts, part, offset=0):

        """
        :param parts: define in how many parts you want to split your display
        :param part: the part in which you want to render text (first part is 0, second is 1, etc.)
        :param offset: define some offset pixel to move strings a little bit (default=0)
        :return:
        """

        x = ((((DISPLAY_WIDTH / parts) / 2) + ((DISPLAY_WIDTH / parts) * part)) - (self.size[0] / 2)) + offset

        self.draw_string(x)

    def draw_string(self, x):

        """
        takes x and y from the functions above and render the font
        """

        TFT.blit(self.font.render(self.string, True, self.color), (x, self.y))