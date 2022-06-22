########################################################################################################################
#                                                      Imports                                                         #
########################################################################################################################
import pygame as pg
from copy import copy
from time import sleep

from new_bci_framework.ui.recording_ui.recording_ui import RecordingUI, BLUE, RED
from new_bci_framework.config.config import Config
from new_bci_framework.recorder.recorder import Recorder


########################################################################################################################
#                                                   Implementation                                                     #
########################################################################################################################
class FeedbackRecordingUI(RecordingUI):
    """
    A subclass of :class:`RecordingUI` which is in charge specifically on the GUI of recording sessions with
    feedback-loops.
    In these sessions, the classifier is already trained so during the recording we can get the prediction of our model
    on the new trials. This GUI, in addition to displaying the paradigm will also display the prediction for each event.
    Notice that this GUI is designed as a soccer penalty-kick game, which is also intended to be an online
    proof of concept.
    @:param Config: a configuration object.
    """
    def __init__(self, config: Config):
        super().__init__(config)

        # Location specification for paradigm images and messages:
        self.msg_loc = self.screen_width / 2, self.screen_height / 3
        self.img_loc = self.screen_width / 2, 4 * self.screen_height / 7

        # BG (soccer field):
        self.field = pg.image.load('new_bci_framework/ui/recording_ui/resources/soccer_field.png')
        self.field = pg.transform.scale(self.field, (self.screen_width, self.screen_height))

        # Prediction representation (a soccer goalie):
        self.goalie = pg.image.load('new_bci_framework/ui/recording_ui/resources/soccer_player.png')
        goalie_size = 80
        self.goalie = pg.transform.scale(self.goalie, (goalie_size, goalie_size))
        self.goalie_center = (self.screen_width / 2 - goalie_size / 2, self.screen_height / 11 - goalie_size / 2)
        self.goalie_loc = self.goalie_center
        goalie_right = [3 * self.screen_width / 4 - goalie_size / 2, self.screen_height / 11 - goalie_size / 2]
        goalie_left = (self.screen_width / 4 - goalie_size / 2, self.screen_height / 11 - goalie_size / 2)
        self.goalie_positions = {'LEFT': goalie_left,
                                 'RIGHT': goalie_right,
                                 'IDLE': self.goalie_center}

        # True label representation (a soccer ball):
        self.ball = pg.image.load('new_bci_framework/ui/recording_ui/resources/soccer_ball.png')
        ball_size = 50
        self.ball = pg.transform.scale(self.ball, (ball_size, ball_size))
        self.ball_center = [self.screen_width / 2 - ball_size / 2, 10 * self.screen_height / 11 - ball_size / 2]
        self.ball_loc = copy(self.ball_center)

    def setup(self):
        """
        see :func:'setup <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.setup>'
        """
        super(FeedbackRecordingUI, self).setup()
        self.__intro()
        pg.display.update()

    def display_event(self, recorder: Recorder, label: str, surface: pg.Surface) -> None:
        """
        see :func:'display_event <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.display_event>'
        In addition, this method adds a 'Processing' screen which waits for preprocessing and prediction on the data
        from the event that was just displayed.
        """
        self.__display_game()
        sleep(self.config.PAUSE_LENGTH)
        self.clear_surface(self.msg_surface)
        sleep(self.config.PAUSE_LENGTH)
        super(FeedbackRecordingUI, self).display_event(recorder, label, surface)
        self.clear_surface(self.msg_surface)
        sleep(self.config.PAUSE_LENGTH)
        self._display_message('Processing')
        sleep(self.config.TRIAL_END_TIME)
        self.clear_surface(self.msg_surface)

    def display_prediction(self, truth: int, prediction: int) -> None:
        """
        see :func:'display_prediction <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.display_event>'
        In this design, the prediction will be shown as a soccer penalty-kick: The ball will move according to the
        true label and the goalie blocks if the prediction is correct.
        """
        label = self.config.MARKERS2LABELS[truth]
        prediction = self.config.MARKERS2LABELS[prediction]
        self.__move_goalie(prediction)
        self.__draw_kick(label)
        prefix, color = ("True", BLUE) if label == prediction else ("False", RED)
        self._display_message(f'{prefix} prediction - {prediction}', color=color)
        sleep(self.config.PAUSE_LENGTH * 2)
        self.__reset_positions()

    def quit(self) -> None:
        """
        see :func:'quit <new_bci_framework.ui.recording_ui.recording_ui.RecordingUI.quit>'
        """
        self.clear_surface(self.screen)
        sleep(self.config.PAUSE_LENGTH)
        self._display_message('Session is over, Thanks!', loc=self.center)
        sleep(self.config.PAUSE_LENGTH)
        super(FeedbackRecordingUI, self).quit()

    def __intro(self) -> None:
        """
        Displays the game intro screens.
        """
        self.screen.fill(self.bg_color)
        self._display_message('Penalty Kick', 100, ((self.screen_width / 2), (self.screen_height / 4)))
        self._display_message('Think LEFT or RIGHT to move', 40, ((self.screen_width / 2), (self.screen_height / 2)))
        sleep(self.config.PAUSE_LENGTH * 2)

        self.screen.fill(self.bg_color)
        description = ['In each round a label will be presented, think as it instructs you.',
                       'The ball will move according to the label.',
                       'The goalie blocks if the prediction is correct.']
        for i, line in enumerate(description):
            self._display_message(line, size=40, loc=((self.screen_width / 2), (self.screen_height / 4) + 40 * i))
        sleep(self.config.PAUSE_LENGTH * 6)

    def __display_game(self) -> None:
        """
        Displays the game board (field, goalie and ball).
        """
        self.screen.blit(self.field, (0, 0))
        self.screen.blit(self.goalie, self.goalie_loc)
        self.screen.blit(self.ball, self.ball_loc)
        pg.display.update()

    def __move_goalie(self, prediction: str) -> None:
        """
        Updates the goalie's position according to the classifier's prediction.
        :param prediction: A string representing the prediction for the event,
        needs to match labels in configuration object.
        """
        self.goalie_loc = self.goalie_positions[prediction]
        self.__display_game()

    def __move_ball(self, dx: float, dy: float) -> None:
        """
        Updates the ball's position in the direction matching the true label.
        :param dx: A float representing the current x location of the ball.
        :param dy: A float representing the current y location of the ball.
        """
        self.ball_loc[0] += dx
        self.ball_loc[1] += dy

    def __draw_kick(self, label) -> None:
        """
        Draws the movements of the goalie and ball to the screen.
        :param label: A string representing the true label of the event, needs to match labels in configuration object.
        """
        x_goalie, y_goalie = self.goalie_positions[label]
        x_ball, y_ball = self.ball_center

        dx, dy = x_goalie - x_ball, y_goalie - y_ball
        iters = 50
        for _ in range(iters):
            self.__move_ball(dx / iters, dy / iters)
            self.__display_game()

    def __reset_positions(self) -> None:
        """
        Resets the positions of the goalie and the ball to the center for the next event.
        """
        self.goalie_loc = self.goalie_center
        self.ball_loc = copy(self.ball_center)
        self.__display_game()




