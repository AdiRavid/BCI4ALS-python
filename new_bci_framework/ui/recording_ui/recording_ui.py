########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import numpy as np
from time import sleep
from typing import Tuple, Optional, Dict

import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder


########################################################################################################################
#                                                      Constant                                                        #
########################################################################################################################
BLACK = (0, 0, 0)
BLUE = (28, 26, 175)
RED = (212, 7, 15)
BG_COLOR = (248, 240, 227)


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class RecordingUI:
    """
    This class is in charge of the experiment's recording phase GUI. It implements a user-interface for running the
    paradigm and collecting data from the subject.
    The session running the recording will also run the GUI.
    Subclasses may represent different GUIs for different recording sessions such as offline, feedback-loop, etc.
    @:param Config: a configuration object.
    """
    def __init__(self, config: Config):
        self.config = config

        # screen width and height:
        self.screen_width = 1000
        self.screen_height = 800
        self.center = (self.screen_width / 2, self.screen_height / 2)
        self.msg_loc = self.screen_width / 2, self.screen_height / 4
        self.img_loc = self.center

        self.msg_surface = pg.Surface((self.screen_width - 100, self.screen_height - 100))

        # colors:
        self.bg_color = BG_COLOR

        # font:
        pg.font.init()
        self.font_name = 'Roboto'
        self.font = pg.font.SysFont(self.font_name, 50)

        # images:
        self.images: Dict[str, pg.image] = {label: pg.image.load(img) for label, img in config.CLASSES_IMS.items()}

        # to be set after init:
        self.screen = None
        self.work: int = np.nan
        self.curr_work: int = 0

    # --------------- Main Methods --------------- #
    def setup(self) -> None:
        """
        Initializes the screen.
        """
        pg.init()
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(self.bg_color)

    def display_event(self, recorder: Recorder, label: str, surface: pg.Surface) -> None:
        """
        The main responsibility of the GUI is to display the trials, this method displays a marker defined by a label
        (which will be obtained from the Paradigm), and synchronizes the display with pushing the label to the board
        stream via the Recorder.
        :param recorder: A recorder object implementing the function push_marker.
        :param label: A string representing the current event, needs to match labels in configuration object (Config).
        :param surface: A pg.Surface object on which the event will be drawn.
        """
        # Ready Phase
        self._display_message(msg=f'READY? Think {label}')
        self._display_image(self.images[label])
        sleep(self.config.PRE_CUE_LENGTH)

        # Push marker to stream
        recorder.push_marker(self.config.LABELS2MARKERS[label])

        # Cue phase
        self.clear_surface(surface)
        self._display_image(self.images[label])
        sleep(self.config.CUE_LENGTH)
        self.clear_surface(surface)

    def display_prediction(self, truth: int, prediction: int) -> None:
        """
        In some cases such as a feedback loop experiment or in co-adaptive learning the GUI will also display the
        prediction obtained for a trial, as the recording is happening. In those cases this method should be
        implemented.
        :param truth: An integer representing the true marker (should be in [1, len(config.CLASSES)]).
        :param prediction: An integer representing the prediction (should be in [1, len(config.CLASSES)]).
        """
        raise NotImplementedError

    def clear_surface(self, surface: pg.Surface) -> None:
        """
        Clears the given surface.
        :param surface:
        :return: A pg.Surface object on which will be cleared.
        """
        surface.fill(self.bg_color)
        self.screen.blit(surface, (50, 50))
        pg.display.flip()

    @staticmethod
    def need_to_quit() -> bool:
        """
        Checks if the user closed the GUI window and quits if so.
        :return: True if the user requested to quit, False otherwise.
        """
        for event in pg.event.get():
            if (event == KEYDOWN and event == K_ESCAPE) or event.type == QUIT:
                return True
        return False

    @staticmethod
    def quit():
        """
        Closes the GUI.
        :return:
        """
        pg.display.quit()
        pg.quit()

    # ---------- Setters for Sessions ---------- #
    def set_work(self, work: int) -> None:
        """
        Allows whoever is running the GUI (probably a Session object) to set the expected work needed - the numbers of
        trials to be recorded.
        :param work: An integer indicating the amount of trials to be recorded.
        """
        self.work = work

    def set_curr_work(self, curr_work):
        """
        Allows whoever is running the GUI (probably a Session object) to set the expected work needed - the numbers of
        trials to be recorded.
        :param curr_work: An integer indicating the trials recorded so far (curr_work <= work).
        """
        self.curr_work = curr_work

    # ---------- GUI helpers ---------- #
    def _display_message(self, msg: str, size: int = 50, loc: Optional[Tuple[float, float]] = None, color=BLACK):
        font = pg.font.SysFont(name=self.font_name, size=size)

        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=self.msg_loc if loc is None else loc)
        self.screen.blit(text, text_rect)

        pg.display.flip()

    def _display_image(self, image: pg.image):
        image_rect = image.get_rect(center=self.img_loc)
        self.screen.blit(image, image_rect)
        pg.display.flip()

    def _blit_long_text(self, text, loc, size=25, color=BLACK):
        font = pg.font.SysFont(name=self.font_name, size=size)
        x, y = loc
        for line in text.splitlines():
            line_surface = font.render(line, True, color)
            line_width, line_height = line_surface.get_size()
            self.msg_surface.blit(line_surface, (x, y))
            y += line_height  # Start on new row.
        pg.display.flip()
