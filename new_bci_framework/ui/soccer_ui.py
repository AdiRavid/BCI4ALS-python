import os
import sys


full_path = os.path.abspath(__file__)
src_index = full_path.rfind('new_bci_framework')
path_to_root = full_path[: src_index]
if path_to_root not in sys.path:
    sys.path.append(path_to_root)
os.chdir(path_to_root)

import pygame as pg
from copy import copy
from time import sleep
from typing import Dict

from new_bci_framework.ui.ui import UI, BLACK
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder

BLUE = (28, 26, 175)
RED = (212, 7, 15)


class SoccerUI(UI):
    def __init__(self, config: Config):
        super().__init__(config)

        self.field = pg.image.load('new_bci_framework/ui/resources/soccer_field.png')
        self.field = pg.transform.scale(self.field, (self.screen_width, self.screen_height))

        self.goalie = pg.image.load('new_bci_framework/ui/resources/soccer_player.png')
        goalie_size = 80
        self.goalie = pg.transform.scale(self.goalie, (goalie_size, goalie_size))
        self.goalie_center = (self.screen_width / 2 - goalie_size / 2, self.screen_height / 11 - goalie_size / 2)
        self.goalie_loc = self.goalie_center

        goalie_right = [3 * self.screen_width / 4 - goalie_size / 2, self.screen_height / 11 - goalie_size / 2]
        goalie_left = (self.screen_width / 4 - goalie_size / 2, self.screen_height / 11 - goalie_size / 2)
        self.goalie_positions = {'LEFT': goalie_left,
                                 'RIGHT': goalie_right,
                                 'IDLE': self.goalie_center}

        self.ball = pg.image.load('new_bci_framework/ui/resources/soccer_ball.png')
        ball_size = 50
        self.ball = pg.transform.scale(self.ball, (ball_size, ball_size))
        self.ball_center = [self.screen_width / 2 - ball_size / 2, 10 * self.screen_height / 11 - ball_size / 2]
        self.ball_loc = copy(self.ball_center)

        self.add_images(config.CLASSES_IMS)
        self.msg_loc = self.screen_width / 2, self.screen_height / 3
        self.img_loc = self.screen_width / 2, 4 * self.screen_height / 7

        self.directions: Dict[int: int] = {'LEFT': -1, 'RIGHT': 1, 'IDLE': 1}

    def setup(self):
        super(SoccerUI, self).setup()
        self.intro()
        pg.display.update()

    def intro(self):
        self.screen.fill(self.bg_color)
        self.display_message('Penalty Kick', 100, ((self.screen_width / 2), (self.screen_height / 4)))
        self.display_message('Think LEFT or RIGHT to move', 40, ((self.screen_width / 2), (self.screen_height / 2)))
        sleep(self.config.PAUSE_LENGTH)

        self.screen.fill(self.bg_color)
        description = '\n'.join(['In each round a label will be presented, think as it instructs you.',
                                 'The ball will move according to the label,',
                                 'the goalie blocks if the prediction is correct.'])
        self.blit_long_text(description, loc=((self.screen_width / 2), (self.screen_height / 2)))
        sleep(self.config.PAUSE_LENGTH * 2)

    def blit_long_text(self, text, loc, size=25, color=BLACK):
        font = pg.font.SysFont(name='Roboto', size=size)
        words = [word.split(' ') for word in text.splitlines()]

        x, y = loc
        for line in words:
            line_surface = font.render(line, True, color)
            line_width, line_height = line_surface.get_size()
            self.msg_surface.blit(line_surface, (x, y))
            y += line_height  # Start on new row.

    def display_game(self):
        self.screen.blit(self.field, (0, 0))
        self.screen.blit(self.goalie, self.goalie_loc)
        self.screen.blit(self.ball, self.ball_loc)
        pg.display.update()

    def display_event(self, recorder: Recorder, label: str, surface: pg.Surface) -> None:
        self.display_game()
        sleep(self.config.PAUSE_LENGTH / 2)
        self.clear_surface(self.msg_surface)
        sleep(self.config.PAUSE_LENGTH / 2)
        super(SoccerUI, self).display_event(recorder, label, surface)
        self.clear_surface(self.msg_surface)
        self.display_message('Processing')
        sleep(self.config.TRIAL_END_TIME)
        self.clear_surface(self.msg_surface)

    def display_prediction(self, true_marker, pred_marker):
        label = self.config.MARKERS2LABELS[true_marker]
        prediction = self.config.MARKERS2LABELS[pred_marker]
        self.move_goalie(prediction)
        self.draw_kick(label)
        prefix, color = ("True", BLUE) if label == prediction else ("False", RED)
        self.display_message(f'{prefix} prediction - {prediction}', color=color)
        sleep(self.config.PAUSE_LENGTH * 2)
        self.reset_game()

    def reset_game(self):
        self.goalie_loc = self.goalie_center
        self.ball_loc = copy(self.ball_center)
        self.display_game()

    def move_goalie(self, prediction):
        self.goalie_loc = self.goalie_positions[prediction]
        self.display_game()

    def draw_kick(self, label):
        x_goalie, y_goalie = self.goalie_positions[label]
        x_ball, y_ball = self.ball_center

        dx, dy = x_goalie - x_ball, y_goalie - y_ball
        iters = 50
        for _ in range(iters):
            self.move_ball(dx / iters, dy / iters)
            self.display_game()

    def move_ball(self, dx, dy):
        self.ball_loc[0] += dx
        self.ball_loc[1] += dy


if __name__ == '__main__':

    config = Config()
    ui = SoccerUI(config)
    ui.setup()
    ui.display_game()
    sleep(2)
    l, p = 'RIGHT', 'RIGHT'
    ui.display_event(Recorder(config), l, ui.msg_surface)
    ui.display_prediction(l, p)
    ui.reset_game()
    sleep(2)
    ui.quit()
