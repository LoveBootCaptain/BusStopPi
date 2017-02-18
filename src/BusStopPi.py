#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import json
import locale
import threading
import time
import pygame
import sys

import requests

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())

pygame.init()

DISPLAY = pygame.display.Info()
# print(DISPLAY)

# DISPLAY_WIDTH = 1920
# DISPLAY_HEIGHT = 1080

DISPLAY_WIDTH = DISPLAY.current_w
DISPLAY_HEIGHT = DISPLAY.current_h


TFT = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
# TFT = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

BLACK = (0, 0, 0)
DARK_GRAY = (10, 10, 10)
GRAY = (43, 43, 43)
WHITE = (255, 255, 255)

RED = (231, 76, 60)
GREEN = (39, 174, 96)
BLUE = (52, 152, 219)

YELLOW = (241, 196, 15)
ORANGE = (238, 153, 18)

pygame.display.set_caption('BusStopPi')

PATH = sys.path[1] + '/src'

print(PATH + '/font/Roboto-Light.ttf')

font_small = pygame.font.Font(PATH + '/font/Roboto-Light.ttf', 30)
font_big = pygame.font.Font(PATH + '/font/Roboto-Light.ttf', 50)

data = {}

next_time = 0
next_line = 'Abc 234'
next_direction = 'Entenhausen'

threads = []
departure_list = ()


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


def convert_timestamp(timestamp, param_string):

    return datetime.datetime.fromtimestamp(int(timestamp)).strftime(param_string)


def check_time():

    global threads, next_time

    thread_1 = threading.Timer(30, check_time)

    thread_1.start()

    threads.append(thread_1)

    next_time = data["departures"][0]["time"]
    next_date = data["departures"][0]["date"]
    next_time = next_date + ' ' + next_time
    next_time = int(time.mktime(datetime.datetime.strptime(next_time, '%d.%m.%y %H:%M').timetuple()))

    time_now = int(time.time())

    time_diff = next_time - time_now

    print('diff: {}'.format(time_diff))

    if time_diff < 0 or time_diff > 86000:

        print('\nUPDATE')
        update_json()

    else:

        print('\nNO UPDATE')
        pass


def update_json():

    global data

    try:

        # response = requests.get('http://sickpi:3000/station/9100013')  # Spittelmarkt
        response = requests.get('http://sickpi:3000/station/9160523')  # Gotlindestr.

        json_data = response.json()

        data = json.loads(json.dumps(json_data[0], indent=4))

        print('\nUPDATE JSON')

        update_departures()

    except (requests.HTTPError, requests.ConnectionError):

        print('\nERROR UPDATE JSON')
        quit_all()


def update_departures():

    global departure_list, next_line, next_direction

    departure_list = data["departures"]

    next_line = data["departures"][0]["line"].replace('Tra', 'Tram')
    next_direction = data["departures"][0]["direction"]


def draw_text_layer():

    global data, next_time, next_line, next_direction, departure_list

    station = data["name"]
    station = station.replace(' (Berlin)', '').replace('U ', '')

    time_now = str(convert_timestamp(time.time(), '%H:%M:%S'))

    print('\n' + station)
    print(time_now)

    DrawImage(PATH + '/icons/haltestelle.png', 10).left()
    DrawString(station, font_big, WHITE, 0).left(55)
    DrawString(time_now, font_big, WHITE, 0).right()

    pygame.draw.line(TFT, ORANGE, (10, 70), (790, 70), 1)

    y = 75

    for departure in departure_list[0:10]:

        line = departure["line"].replace('Tra', 'Tram')
        dep_time = departure["time"]
        direction = departure["direction"]

        if 'Tram' in line:
            # print('Tram')
            DrawImage(PATH + '/icons/tram.png', y + 8).left()

        elif 'Bus' in line:
            # print('Bus')
            DrawImage(PATH + '/icons/bus.png', y + 8).left()

        elif 'U' in line:
            # print('UBahn')
            DrawImage(PATH + '/icons/ubahn.png', y + 8).left()

        output = str(line + '   -   ' + dep_time + '    -   ' + direction)
        print(output)

        line = line.replace('Tram ', '').replace('Bus ', '')
        direction = direction.replace(' (Berlin)', '').replace('[U5]', '').replace(' bitte umsteige', '')

        DrawString(line, font_small, ORANGE, y).left(35)
        DrawString(dep_time, font_small, ORANGE, y).left(115)
        DrawString(direction, font_small, ORANGE, y).left(215)

        y += 30

    y += 10

    pygame.draw.line(TFT, ORANGE, (10, 390), (790, 390), 1)

    time_now = int(time.time())

    time_diff = next_time - time_now

    print('\ndiff: {}'.format(time_diff))

    time_diff_str = time.strftime('%M m %S s', time.gmtime(abs(time_diff)))

    next_direction = next_direction.replace(' (Berlin)', '').replace('[U5]', '').replace(' bitte umsteige', '')

    if time_diff < 0 or time_diff > 86000:

        update_message_1 = '{} sollte um {} Uhr'.format(
            next_line,
            convert_timestamp(next_time, '%H:%M')
        )

        update_message_2 = 'nach {} fahren'.format(
            next_direction
        )

        print('\n' + update_message_1)
        print(update_message_2)

    else:

        update_message_1 = '{} kommt um {} Uhr'.format(
            next_line,
            convert_timestamp(next_time, '%H:%M')
        )

        update_message_2 = 'in {} nach {}'.format(
            time_diff_str,
            next_direction
        )

        print('\n' + update_message_1)
        print(update_message_2)

    if 'Bus' in update_message_1:

        # print('BUS')
        DrawImage(PATH + '/icons/big_bus.png', 400).left()

    elif 'Tram' in update_message_1:

        # print('TRAM')
        DrawImage(PATH + '/icons/big_tram.png', 400).left()

    else:

        print('\nNOTHING')

    DrawString(update_message_1, font_small, WHITE, 395).left(70)
    DrawString(update_message_2, font_small, WHITE, 430).left(70)


def update_data():

    update_json()
    check_time()


def draw_to_tft():

    TFT.fill(BLACK)

    draw_text_layer()

    pygame.display.update()

    time.sleep(1)


def quit_all():

    global threads

    for thread in threads:
        thread.cancel()
        thread.join()

    pygame.quit()
    quit()


def loop():

    update_data()

    running = True

    while running:

        draw_to_tft()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

                quit_all()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    running = False

                    quit_all()

                elif event.key == pygame.K_SPACE:

                    print('\nSPACE')

    quit_all()


if __name__ == '__main__':

    try:

        loop()

    except KeyboardInterrupt:

        quit_all()

