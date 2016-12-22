#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from modules import DISPLAY_WIDTH, TFT


class DrawImage:

    def __init__(self, image_path, y):

        """
        :param image_path: the path to the image you want to render
        :param y: the y-postion of the image you want to render
        """

        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.y = y
        self.size = self.image.get_rect().size

    def left(self, offset=0):

        """
        :param offset: define some offset pixel to move strings a little bit (default=0)
        :return:
        """

        x = 10 + offset

        self.draw_image(x)

    def right(self, offset=0):

        """
        :param offset: define some offset pixel to move strings a little bit (default=0)
        :return:
        """

        x = (DISPLAY_WIDTH - self.size[0] - 10) - offset

        self.draw_image(x)

    def center(self, parts, part, offset=0):

        """
        :param parts: define in how many parts you want to split your display
        :param part: the part in which you want to render text (first part is 0, second is 1, etc.)
        :param offset: define some offset pixel to move strings a little bit (default=0)
        :return:
        """

        x = int(((((DISPLAY_WIDTH / parts) / 2) + ((DISPLAY_WIDTH / parts) * part)) - (self.size[0] / 2)) + offset)

        self.draw_image(x)

    def draw_image(self, x):

        """
        takes x from the functions above and the y from the class to render the image
        """

        TFT.blit(self.image, (x, self.y))