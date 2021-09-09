import hand_recognizer as recognizer
import CONSTANTS

import cv2
import pyautogui


class RightHand:
    def __init__(self, aScreenRes, aControlType):
        self.screenRes = aScreenRes
        self.control_type = aControlType
        self.positions = [None] * 4
        self.num_frames = 0
        self.last_x, self.last_y = 0, 0

        # Disables failsafe for moving mouse to a corner of the screen
        pyautogui.FAILSAFE = False


    @staticmethod
    def __smoothMousePosition(aList, aNewValue):
        """
        Copies every value to previous index, places aNewValue on last index and returns the average values.
        :param aList: Python list of tuples in which the previous screen coordinates for the mouse are stored.
        :param aNewValue: Tuple with the new screen coordinates for the mouse.
        :return: int, int --> average X position, average Y position
        """
        # To calculate average X and Y
        sum_x, sum_y = 0, 0

        # If the list is not full, find first empty index and replace with new value
        if aList[-1] is None:
            for i in range(len(aList)):
                if aList[i] is None:
                    sum_x += aNewValue[0]
                    sum_y += aNewValue[1]
                    new_x = round(sum_x / (i+2))
                    new_y = round(sum_y / (i+2))

                    aList[i] = (new_x, new_y)
                    return new_x, new_y
                else:
                    sum_x += aList[i][0]
                    sum_y += aList[i][1]

        # If it's full, move every value to its position-1
        for i in range(len(aList) - 1):
            aList[i] = aList[i + 1]
            sum_x += aList[i][0]
            sum_y += aList[i][1]

        # Calculate the new average mouse position with the input values
        sum_x += aNewValue[0]
        sum_y += aNewValue[1]
        new_x = round(sum_x / len(aList))
        new_y = round(sum_y / len(aList))

        # Add the new rounded position to the last index of the list
        aList[-1] = (new_x, new_y)

        return new_x, new_y

    def transformToScreenSize(self, aFingerX, aFingerY):
        """
        Transform finger coordinates from Mediapipe's system to correspondent screen coordinates.
        :param aFingerX: X coordinate from landmark
        :param aFingerY: Y coordinate from landmark
        :return: int, int --> screen X coordinate, screen Y coordinate
        """
        if self.screenRes is None:
            raise Exception("Global variable ScreenRes type is None. ScreenRes value: {}".format(self.screenRes))

        # Sometimes MediaPipe can detect the center of the landmark outside the screen
        # if the finger is too close to the edge
        if aFingerX < 0: aFingerX = 0
        if aFingerY < 0: aFingerY = 0

        mouseX = aFingerX * self.screenRes.width
        mouseY = aFingerY * self.screenRes.height
        return round(mouseX), round(mouseY)


    def trackpadMove(self, aHandX, aHandY, aNumberOfFingers):
        """
        Move cursor across screen with a distance proportional to the number of fingers extended.
        :param aHandX: hand's center X coordinate
        :param aHandY: hand's center Y coordinate
        :param aNumberOfFingers: number of fingers extended
        :return: None
        """
        if self.last_x == 0 and self.last_y == 0:
            self.last_x, self.last_y = aHandX, aHandY
            return

        # Calculate distance traveled by hand
        distX = aHandX - self.last_x
        distY = aHandY - self.last_y

        # Update last known hand X and Y coordinates
        self.last_x, self.last_y = aHandX, aHandY

        # Record current screen cursor X and Y coordinates
        mouseCurrent = pyautogui.position()

        multiplier = 1
        if aNumberOfFingers is 3:
            multiplier = 2
        elif aNumberOfFingers is 4:
            multiplier = 3
        elif aNumberOfFingers is 5:
            multiplier = 5

        # Smooth the mouse movement
        #mouse_x, mouse_y = self._smoothMousePosition(self.positions, (mouseCurrent.x, mouseCurrent.y))

        # Make the cursor move the same distance as the hand
        #pyautogui.moveTo(mouse_x + distX, mouse_y + distY, _pause=False)
        pyautogui.moveTo(mouseCurrent.x + multiplier*distX, mouseCurrent.y + aNumberOfFingers*distY, _pause=False)


    def run(self, aHandLandmarks, aFrame):
        #print("----------------RIGHT-----------------")
        if self.control_type == CONSTANTS.MouseControl.Raw:       # Exact
            # Get the relative finger coordinates from mediapipe's system (between 0.0 and 1.0)
            finger_x, finger_y = recognizer.getFingerPoint(aHandLandmarks)

            # Convert relative coordinates to position in screen
            screen_x, screen_y = self.transformToScreenSize(finger_x, finger_y)

            # Attempt to reduce noise
            mouse_x, mouse_y = self.__smoothMousePosition(self.positions, (screen_x, screen_y))

            #print("Mouse X:", mouse_x)
            pyautogui.moveTo(mouse_x, mouse_y, _pause=False)
        elif self.control_type == CONSTANTS.MouseControl.Trackpad:  # Trackpad
            # Get the relative hand coordinates from mediapipe's system (between 0.0 and 1.0)
            hand_x, hand_y = recognizer.getHandCenter(aHandLandmarks)

            # Convert relative coordinates to position in screen
            screen_x, screen_y = self.transformToScreenSize(hand_x, hand_y)

            # Get the number of fingers
            isSuccessful, fingersCount = recognizer.calculateFingers(aHandLandmarks)

            if isSuccessful and fingersCount >= 2:
                self.trackpadMove(screen_x, screen_y, fingersCount)
            else:
                # Reset last_x and last_y to 0 so they don't interfere with distance traveled
                # math on the very first occurrence (when hand re-enters the ROI)
                self.last_x, self.last_y = 0, 0

            try:
                """# To draw the hand skeleton
                mp_drawing = mp.solutions.drawing_utils
                mp_hands = mp.solutions.hands"""

                cv2.putText(aFrame, "Number: {}".format(str(fingersCount)),
                            (int(self.screenRes.width/2 + 50), int(self.screenRes.height/2 + 40)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                """mp_drawing.draw_landmarks(
                    aFrame, aHandLandmarks, mp_hands.HAND_CONNECTIONS)"""
            except Exception as e:
                print(e)
        elif self.control_type == CONSTANTS.MouseControl.Vector:  # Vector
            pass
        else:
            raise Exception("CONTROL MOUSE TYPE UNDEFINED")
