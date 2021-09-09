import hand_recognizer as recognizer
import CONSTANTS

import cv2
import pyautogui
import time

def PrintException():
    import sys
    import linecache

    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


class LeftHand:
    def __init__(self, aMainWindow=None, aNotifier=None):
        self.num_frames = 0
        self._lastTime = time.time() * 1000
        self._lastGesture = None
        self.ui_MainWindow = aMainWindow
        self.ui_videoWindow = None
        self.notifier = aNotifier
        self.notifier.subscribe('set_videoplayer_window', self.setVideoWindow)


    def setVideoWindow(self, aVideoWindow=None):
        self.ui_videoWindow = aVideoWindow


    def mouseActions(self, aGesture):
        # To test if the gesture is the same after 2 seconds
        if time.time()*1000 - self._lastTime < 2000:
            return

        # If it's a different gesture then do nothing,
        # update _lastGesture and update timer
        if aGesture != self._lastGesture:
            self._lastTime = time.time() * 1000
            self._lastGesture = aGesture
            return

        #region  -------- Fist
        if aGesture == CONSTANTS.Poses.Fist:
            # get name of the widget that we're interacting with
            if self.ui_MainWindow is not None:
                name = None

                # if video player window is open
                if self.ui_videoWindow is not None:
                    name = self.ui_videoWindow.getWidgetAtCursor()

                # if it doesn't exist on the video player, check main interface
                if name is None:
                    name = self.ui_MainWindow.getWidgetAtCursor()

                # if cursor is on top of video player window
                if "videoplayer_" in name:
                    # decrease the volume
                    self.notifier.notify('videoplayer_volume_down')
                elif "section_" in name:
                    pyautogui.click()
                    print("Left click")
        #endregion

        #region  -------- Three
        elif aGesture == CONSTANTS.Poses.Three:
            # get name of the widget that we're interacting with
            if self.ui_MainWindow is not None:
                name = None

                # if video player window is open
                if self.ui_videoWindow is not None:
                    name = self.ui_videoWindow.getWidgetAtCursor()

                # if it doesn't exist on the video player, check main interface
                if name is None:
                    name = self.ui_MainWindow.getWidgetAtCursor()

                # if cursor is on top of video player window
                if "videoplayer_" in name:
                    # play/pause the video
                    self.notifier.notify('videoplayer_play_or_pause')
                elif "section_" in name:
                    # scroll up
                    self.notifier.notify('scroll_vertically', False)
        #endregion

        #region  -------- Five
        elif aGesture == CONSTANTS.Poses.Five:
            # if mainwindow exists
            if self.ui_MainWindow is not None:
                name = self.ui_MainWindow.getWidgetAtCursor()

                # if mouse is on top of <Genre> Movies area (e.g. Action Movies)
                if "section_" in name:
                    # scroll the movie section to the left
                    self.notifier.notify('scroll_section', name)
        #endregion

        #region  -------- Telephone
        elif aGesture == CONSTANTS.Poses.Telephone:
            # get name of the widget that we're interacting with
            if self.ui_MainWindow is not None:
                name = None

                # if video player window is open
                if self.ui_videoWindow is not None:
                    name = self.ui_videoWindow.getWidgetAtCursor()

                # if it doesn't exist on the video player, check main interface
                if name is None:
                    name = self.ui_MainWindow.getWidgetAtCursor()

                # if cursor is on top of video player window
                if "videoplayer_" in name:
                    # close the video player window
                    self.notifier.notify('videoplayer_close')
                # if cursor is on top of '<Category> Movies' area (e.g. Action Movies)
                elif "section_" in name:
                    # scroll the movie section to the left
                    self.notifier.notify('scroll_section', name, False)
        #endregion

        #region -------- Rock
        elif aGesture == CONSTANTS.Poses.Rock:
            # get name of the widget that we're interacting with
            if self.ui_MainWindow is not None:
                name = None

                # if video player window is open
                if self.ui_videoWindow is not None:
                    name = self.ui_videoWindow.getWidgetAtCursor()

                # if it doesn't exist on the video player, check main interface
                if name is None:
                    name = self.ui_MainWindow.getWidgetAtCursor()

                if "videoplayer_" in name:
                    # increase the volume
                    self.notifier.notify('videoplayer_volume_up')
                elif "section_" in name:
                    # scroll down
                    self.notifier.notify('scroll_vertically')
        #endregion

        # Update _lastGesture and timer
        self._lastTime = time.time() * 1000
        self._lastGesture = aGesture


    def run(self, aHandLandmarks, aFrame):
        #print("##############LEFT################")
        try:
            # Get the output gesture
            gesture = recognizer.getHandGesture(aHandLandmarks, False)

            # Activate corresponding mouse action
            if gesture is not CONSTANTS.Poses.ERROR:
                self.mouseActions(gesture)

            cv2.putText(aFrame, "hand pose: {}".format(gesture.value), (15, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        except Exception:
            cv2.putText(aFrame, "hand pose: error", (15, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            print("\tLEFT run")
            PrintException()
