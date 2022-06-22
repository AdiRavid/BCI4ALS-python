########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import numpy as np
import pygame as pg
from time import sleep

from new_bci_framework.ui.recording_ui.recording_ui import RecordingUI
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class OfflineRecordingUI(RecordingUI):
    """
    A subclass of :class:`RecordingUI` which is in charge specifically on the GUI of offline recording sessions.
    @:param Config: a configuration object.
    """
    def __init__(self, config: Config):
        super().__init__(config)

        # Progress bar:
        self.bar_color = '#9b2226'
        self.bar_w = 400
        self.bar_h = 20
        self.bar_x = self.screen_width / 2 - self.bar_w / 2
        self.bar_y = self.screen_height * 0.9 - self.bar_h / 2

    def setup(self) -> None:
        """
        see :func: 'setup <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.setup>'
        """
        pg.display.set_caption('Offline Session')
        super(OfflineRecordingUI, self).setup()

        self._display_message('Hello, training session will start soon', loc=self.center)
        sleep(self.config.PAUSE_LENGTH * 2)

        self.screen.fill(self.bg_color)
        self._display_message('Starting now', loc=self.center)

    def display_event(self, recorder: Recorder, label: str, surface: pg.Surface) -> None:
        """
        see :func:'display_event <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.display_event>'
        """
        sleep(self.config.PAUSE_LENGTH)
        super(OfflineRecordingUI, self).display_event(recorder, label, surface)

    def clear_surface(self, surface: pg.Surface) -> None:
        """
        see :func:'clear_surface <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.clear_surface>'
        In addition, in this class a progress bar is maintained and is updated when this method is called.
        """
        self.__update_progress_bar()
        super(OfflineRecordingUI, self).clear_surface(surface)

    def quit(self) -> None:
        """
        see :func:'quit <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.quit>'
        """
        self.curr_work = self.work
        self.clear_surface(self.screen)
        sleep(self.config.PAUSE_LENGTH)
        self._display_message('Session is over, Thanks!', loc=self.center)
        sleep(self.config.PAUSE_LENGTH)
        super(OfflineRecordingUI, self).quit()

    def __update_progress_bar(self) -> None:
        """
        Updates the progress bar which gives the subject an indication of how many trials he has passed out of total.
        """
        # Border:
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w, self.bar_h), 1)

        # Bar
        if self.work == 0 or np.isnan(self.work):
            progress = 1
        else:
            progress = 1 - (self.work - self.curr_work) / self.work
        pg.draw.rect(self.screen, self.bar_color, pg.Rect(self.bar_x, self.bar_y, self.bar_w * progress, self.bar_h))

