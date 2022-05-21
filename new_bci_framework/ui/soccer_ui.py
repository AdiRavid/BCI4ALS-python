import os
import sys

full_path = os.path.abspath(__file__)
src_index = full_path.rfind('new_bci_framework')
path_to_root = full_path[: src_index]
if path_to_root not in sys.path:
    sys.path.append(path_to_root)
os.chdir(path_to_root)

import pygame as pg
from time import sleep

from new_bci_framework.ui.ui import UI
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder


class SoccerUI(UI):
    def __init__(self, config: Config):
        super().__init__(config)

        self.field = pg.image.load('new_bci_framework/ui/resources/soccer_field.png')
        self.field = pg.transform.scale(self.field, (self.screen_width, self.screen_height))

        self.goalie = pg.image.load('new_bci_framework/ui/resources/soccer_player.png')
        self.goalie = pg.transform.scale(self.goalie, (80, 80))
        self.goalie_center = (self.screen_width / 2 - 35, self.screen_height / 11)

        self.ball = pg.image.load('new_bci_framework/ui/resources/soccer_ball.png')
        self.ball = pg.transform.scale(self.ball, (50, 50))
        self.ball_center = (self.screen_width / 2 - 30, 10 * self.screen_height / 11)

        self.add_images(config.CLASSES_IMS)
        self.msg_loc = self.screen_width / 2, self.screen_height / 3
        self.img_loc = self.screen_width / 2, 4 * self.screen_height / 7

        self.right_detected = False
        self.left_detected = False

    def setup(self):
        pg.init()
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        self.intro()
        sleep(self.config.PAUSE_LENGTH * 2)

        self.screen.blit(self.field, (0, 0))
        self.screen.blit(self.goalie, self.goalie_center)
        self.screen.blit(self.ball, self.ball_center)

        pg.display.update()

    def intro(self):
        self.screen.fill(self.bg_color)
        largeText = pg.font.SysFont("courier", 100)
        TextSurf, TextRect = self.text_objects("Penalty Kick", largeText)
        TextRect.center = ((self.screen_width / 2), (self.screen_height / 4))
        self.screen.blit(TextSurf, TextRect)
        largeText = pg.font.SysFont("courier", 40)
        TextSurf, TextRect = self.text_objects("Think LEFT or RIGHT to block", largeText)
        TextRect.center = ((self.screen_width / 2), (self.screen_height / 2))
        self.screen.blit(TextSurf, TextRect)
        pg.display.update()

    def display_event(self, recorder: Recorder, label: str) -> None:
        sleep(self.config.PAUSE_LENGTH)

        self.display_message(msg=f'READY? Think {label}')
        self.display_image(self.images[label])
        sleep(self.config.PRE_CUE_LENGTH)

        recorder.push_marker(self.config.TRIAL_LABELS[label])

        self.clear_screen()
        self.display_image(self.images[label])
        sleep(self.config.CUE_LENGTH)
        self.clear_screen()

    def clear_screen(self):
        pass

    def text_objects(self, text, font, color='black'):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


if __name__ == '__main__':

    config = Config()
    ui = SoccerUI(config)
    ui.setup()
    ui.display_event(Recorder(config), 'RIGHT')
    ui.quit()
